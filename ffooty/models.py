# -*- coding: utf-8 -*-

import calendar
import datetime
from urllib import urlopen

from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from bs4 import BeautifulSoup


class NameMixin(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        abstract = True
        app_label = 'ffooty'

    def __unicode__(self):
        return self.name


class TeamObjectManager(models.Manager):
    """
    Custom manager to exclude non active teams.
    """
    def get_queryset(self):
        return super(TeamObjectManager, self).get_queryset().exclude(is_active=False)


class Team(NameMixin):
    manager = models.ForeignKey(User)
    score = models.IntegerField(default=0)
    funds = models.DecimalField(decimal_places=1, max_digits=4, default=0)
    loss = models.DecimalField(decimal_places=1, max_digits=4, default=0,
                               help_text='Cumulative loss made selling players back to pool')
    winnings = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    line_up_is_valid = models.BooleanField(default=False)
    cup_start_position = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)  # is the team active in the current season

    objects = models.Manager()
    active_objects = TeamObjectManager()

    class Meta:
        ordering = ['manager__username']

    @property
    def latest_weekly_score(self):
        from ffooty.functions import get_week
        week = get_week()
        return TeamWeeklyScore.objects.filter(team=self).order_by('-week').first().value

    @property
    def ex_players(self):
        """Return all players that have a PlayerScore record for this team."""
        all_player_ids = PlayerScore.objects.filter(
            team=self
        ).values_list(
            'player', flat=True
        ).order_by(
            'player'
        ).distinct()
        return Player.objects.filter(id__in=all_player_ids).exclude(team=self)

    def __unicode__(self):
        return '{} ({})'.format(self.name, self.manager)

    def update_funds(self):
        initial_funds = Constant.objects.get(name='INITIAL_FUNDS')
        transfer_funds = Constant.objects.get(name='TEAM_TRANSFER_FUNDS')
        funds = initial_funds.value + transfer_funds.value - self.loss
        for p in self.players.all():
            funds -= p.sale
        self.funds = funds
        self.save()

    def validate_line_up(self):
        self.line_up_is_valid = all([
            (self.players.filter(position=Player.GKP,
                                 status=Player.FIRST_TEAM).count() == 1),
            (self.players.filter(position=Player.DEF,
                                 status=Player.FIRST_TEAM).count() == 4),
            (self.players.filter(position=Player.MID,
                                 status=Player.FIRST_TEAM).count() == 4),
            (self.players.filter(position=Player.STR,
                                 status=Player.FIRST_TEAM).count() == 2),
            (self.players.filter(position=Player.GKP,
                                 status=Player.RESERVE).count() == 1),
            (self.players.filter(position=Player.DEF,
                                 status=Player.RESERVE).count() == 1),
            (self.players.filter(position=Player.MID,
                                 status=Player.RESERVE).count() == 1),
            (self.players.filter(position=Player.STR,
                                 status=Player.RESERVE).count() == 1)
        ])
        self.save()
        return self.line_up_is_valid

    def update_total_score(self):
        # update the team total score
        total_score = TeamWeeklyScore.objects.filter(
            team=self
        ).aggregate(models.Sum('value'))['value__sum']
        self.score = total_score or 0
        self.save()

    def process_motm(self, win=True):
        """
        Add or deduct MOTM prize.
        :param win: bool, True = award MotM prize, False = cancel
        :return: None
        """
        prize = Constant.objects.get(name='MOTM_PRIZE').value
        if win:
            self.winnings += prize
        else:
            self.winnings -= prize
        self.save()


class PremTeam(NameMixin):
    is_prem = models.BooleanField(default=True)
    code = models.CharField(max_length=3, unique=True)
    web_code = models.IntegerField(null=True)

    def __unicode__(self):
        return self.code


class PlayerManager(models.Manager):
    def goalkeepers(self):
        return super(PlayerManager, self).get_queryset().filter(code__lt=2000)

    def defenders(self):
        return super(PlayerManager, self).get_queryset().filter(code__range=(2000, 2999))

    def midfielders(self):
        return super(PlayerManager, self).get_queryset().filter(code__range=(3000, 3999))

    def strikers(self):
        return super(PlayerManager, self).get_queryset().filter(code__gte=4000)


class Player(models.Model):
    GKP = 'G'
    DEF = 'D'
    MID = 'M'
    STR = 'S'

    POSITION = (
        (GKP, 'GKP'),
        (DEF, 'DEF'),
        (MID, 'MID'),
        (STR, 'STR'),
    )

    WEB_GKP = 1
    WEB_DEF = 2
    WEB_MID = 3
    WEB_STR = 4

    AVAILABLE = 'A'
    FIRST_TEAM = 'F'
    RESERVE = 'R'
    SQUAD = 'S'

    STATUS = (
        (AVAILABLE, 'Available'),
        (FIRST_TEAM, 'First Team'),
        (RESERVE, 'Reserve'),
        (SQUAD, 'Squad'),
    )

    # sql for ordering by position in a custom (non-alphbetical) ordering
    CASE_SQL = "case when position='G' then 1 when position='D' then 2 when position='M' then 3 when position='S' then 4 end"

    name = models.CharField(max_length=50)
    position = models.CharField(null=True, blank=True, max_length=1, choices=POSITION)
    status = models.CharField(blank=True, max_length=1, choices=STATUS, default=AVAILABLE)
    code = models.IntegerField(null=True, blank=True)
    web_code = models.IntegerField(unique=True, null=True)
    team = models.ForeignKey(Team, null=True, blank=True, related_name='players')
    prem_team = models.ForeignKey(PremTeam, related_name='players')
    value = models.DecimalField(decimal_places=1, max_digits=3, null=True, blank=True)
    sale = models.DecimalField(decimal_places=1, max_digits=3, null=True, blank=True)
    total_score = models.IntegerField(default=0)
    last_years_total = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)  # is active in the Telegraph website
    is_new = models.BooleanField(default=False)  # has been added in the most recent update
    appearances = models.IntegerField(default=0)  # track no. of appearances

    # managers (the first will be the default manager)
    objects = PlayerManager()

    class Meta:
        ordering = ['code']
        unique_together = ('name', 'code',)

    def __unicode__(self):
        return '{} {} {} {} {}'.format(self.code, self.position, self.name.encode('utf-8'), self.prem_team, self.value)

    def __str__(self):
        return '{} {} {} {} {}'.format(self.code, self.position, self.name.encode('utf-8'), self.prem_team, self.value)

    @property
    def details(self, *args, **kwargs):
        return "{}, {}, £{}m".format(self.name.encode('utf-8'), self.team, self.value)

    @property
    def auction_nomination_managers(self):
        # return a string of manager names, those with only 2 are anonymised
        nom_list = [nom.team.manager.username for nom in self.auctionnomination_set.all()]
        if len(nom_list) == 2:
            return '[2]'
        else:
            return ', '.join(nom_list)

    @property
    def admin_auction_nomination_managers(self):
        # return a list of manager names
        return [nom.team.manager.username for nom in self.auctionnomination_set.all()]

    @property
    def total_score_counted(self, team=None):
        """
        Return the total score counted for the player.

        The default behaviour is to return the total for the current team, but
        this can be overridden using the optional ``team`` parameter.

        :param Team team: (optional) define another team to get the total for
        """
        # default to the current team if none provided
        if not team:
            team = self.team
        return self.scores.filter(team=team, is_counted=True).aggregate(models.Sum('value'))['value__sum']

    def return_to_pool(self, loss_offset=0):
        """
        Move the player from a team back into the available pool of players.
        """
        # TODO - move this to a sell() method then create the return to pool as a wrapper
        if self.team:
            # add any losses to the team
            loss = self.sale - self.value + loss_offset
            self.team.loss += loss
            self.team.funds += self.value
            self.team.save()
            # reset the player's team and status
            self.team = None
            self.status = self.AVAILABLE
            self.save()
            return loss
        else:
            print "return_to_pool(): {} is not owned by a team!".format(self.name.encode('utf-8'))

    def update_transfers(self):

        # get the bids in descending order
        tns = TransferNomination.objects.filter(player=self).order_by('-bid')

        print "update_transfers: tns = ", tns

        # if there's only one bid, set it to LIST unless it's already been ACCEPTED or PASSED
        # those nominations set to LIST will also have bids adjusted to list price
        if tns.count() == 1:
            nom = tns.exclude(
                status__in=[TransferNomination.ACCEPTED, TransferNomination.PASSED]
            ).first()
            if nom:
                nom.status = TransferNomination.LIST
                nom.bid = self.value
                nom.save()
            return

        # check for an accepted bid
        accepted = tns.filter(status=TransferNomination.ACCEPTED).first()

        # if one has been accepted, set all OUTBID to FAILED and return
        if accepted:
            outbid_nominations = tns.filter(status=TransferNomination.OUTBID)
            for nom in outbid_nominations:
                nom.status = TransferNomination.FAILED
                nom.save()
            return

        # get PENDING, OUTBID and HIGHEST nominations to process:
        noms_to_update = tns.filter(status__in=[
            TransferNomination.PENDING, TransferNomination.OUTBID, TransferNomination.HIGHEST
        ])

        if noms_to_update.exists():
            # set the HIGHEST:
            highest_nom = noms_to_update[0]
            highest_nom.status = TransferNomination.HIGHEST
            highest_nom.save()

            # set any remaining to OUTBID
            for nom in noms_to_update[1:]:
                nom.status = TransferNomination.OUTBID
                nom.save()

        return


class Week(models.Model):
    number = models.IntegerField(unique=True)
    date = models.DateField()
    is_cup = models.BooleanField(default=False)

    class Meta:
        ordering = ['number']

    def __unicode__(self):
        return "Wk{}: {}-{}".format(self.number, self.date.day, self.date.month)


class ScoreBaseModel(models.Model):
    value = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.value


class PlayerScore(ScoreBaseModel):
    player = models.ForeignKey(Player, related_name='scores')
    team = models.ForeignKey(Team, null=True, blank=True)
    week = models.ForeignKey(Week)
    is_reserve = models.BooleanField(default=False)
    is_squad = models.BooleanField(default=False)
    is_counted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('player', 'week', 'team',)

    @property
    def display_value(self):
        if self.value is None:
            return '#'
        elif self.is_counted:
            return self.value
        else:
            return '*{}*'.format(self.value)

    def __unicode__(self):
        return "{}: {}: (week {}): {} - {}".format(
            self.player.code, self.player.name, self.week.number, self.value,
            ('Y' if self.is_counted else 'N')
        )


class PlayerTeamScore(ScoreBaseModel):
    team = models.ForeignKey(Team, related_name='player_team_scores')
    player = models.ForeignKey(Player, related_name='player_team_scores')

    def update(self):
        value = PlayerScore.objects.filter(
            team=self.team, player=self.player, is_counted=True
        ).aggregate(models.Sum('value'))['value__sum']
        self.value = value or 0
        self.save()


class TeamWeeklyScore(ScoreBaseModel):
    team = models.ForeignKey(Team, related_name='weekly_scores')
    week = models.ForeignKey(Week)

    class Meta:
        unique_together = ('team', 'week',)

    def __unicode__(self):
        return "{} (week {}): {}".format(
            self.team.name, self.week, self.value
        )

    def update(self):
        player_scores = PlayerScore.objects.filter(team=self.team, week=self.week, is_counted=True)
        self.value = player_scores.aggregate(models.Sum('value'))['value__sum']
        self.save()


class TeamMonthlyScore(ScoreBaseModel):
    team = models.ForeignKey(Team, related_name='monthly_scores')
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    prize_awarded = models.BooleanField(default=False, blank=True)

    class Meta:
        unique_together = ('team', 'month',)

    def __unicode__(self):
        return "{} ({}): {}".format(
            self.team.name, calendar.month_name[self.month], self.value
        )

    def update(self):
        from .functions import get_weeks_and_scores_for_month
        _weeks, _player_scores, weekly_scores = get_weeks_and_scores_for_month(
            team=self.team, month=self.month
        )

        monthly_score = weekly_scores.aggregate(models.Sum('value'))['value__sum']
        self.value = monthly_score or 0
        self.save()


class TeamTotalScore(ScoreBaseModel):
    team = models.ForeignKey(Team)

    def __unicode__(self):
        return "{} (total): {}".format(self.team.name, self.value)


class TeamTotalScoreArchive(ScoreBaseModel):
    """
    Model for archiving season total scores for teams.
    """
    team = models.ForeignKey(Team)

    YEAR_CHOICES = []
    for year in range(2014, 2030):
        YEAR_CHOICES.append((year, year))

    year = models.IntegerField(
        max_length=4,
        choices=YEAR_CHOICES,
        default=datetime.datetime.now().year
    )

    def __unicode__(self):
        return "{} (total for {}): {}".format(self.team.name, self.year, self.value)



class TeamTablePosition(models.Model):
    """
    Model to track team position in league table.
    """
    team = models.ForeignKey(Team)
    current_week = models.IntegerField()
    previous_week = models.IntegerField()


class Window(models.Model):
    AUCTION_NOMINATION = 'N'
    AUCTION = 'A'
    SQUAD_CHANGE = 'S'
    TRANSFER_NOMINATION = 'T'
    TRANSFER_CONFIRMATION = 'C'

    TYPES = (
        (AUCTION_NOMINATION, 'Auction Nomination'),
        (AUCTION, 'Auction'),
        (SQUAD_CHANGE, 'Squad Change'),
        (TRANSFER_NOMINATION, 'Transfer Nomination'),
        (TRANSFER_CONFIRMATION, 'Transfer Confirmation'),
    )

    open_from = models.DateTimeField()
    deadline = models.DateTimeField()
    type = models.CharField(max_length=1, choices=TYPES, default=SQUAD_CHANGE)

    def __unicode__(self):
        return "{}: {} to {}".format(self.get_type_display(),
                                     self.open_from,
                                     self.deadline)


class NominationMixin(models.Model):
    team = models.ForeignKey(Team)
    player = models.ForeignKey(Player)

    class Meta:
        abstract = True
        # unique_together = ('team', 'player',)


class AuctionNomination(NominationMixin):

    passed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('team', 'player',)


class IllegalNominationOperationException(Exception):
    pass


class TransferNomination(NominationMixin):
    PENDING = 'N'       # waiting initial assignment ('N' = New)
    HIGHEST = 'H'       # highest bid (either from outset or following a 'pass')
    JOINT = 'J'         # joint highest bid with one or more other manager(s)
    LIST = 'L'          # sole bid, player is available at list
    OUTBID = 'O'        # a higher bid is currently being considered
    PASSED = 'P'        # manager has passed on the bid
    ACCEPTED = 'A'      # bid confirmed
    FAILED = 'F'        # other manager's bid has been confirmed

    STATUSES = (
        (PENDING, 'Pending'),
        (HIGHEST, 'Highest'),
        (JOINT, 'Joint Highest'),
        (LIST, 'List'),
        (OUTBID, 'Outbid'),
        (PASSED, 'Passed'),
        (ACCEPTED, 'Accepted'),
        (FAILED, 'Bid Failed'),
    )

    status = models.CharField(max_length=1, choices=STATUSES, default=PENDING)
    transfer_window = models.ForeignKey(Window, blank=True, null=True)
    bid = models.DecimalField(decimal_places=1, max_digits=3, null=True)
    priority = models.IntegerField(null=True, blank=True)
    processed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('team', 'player', 'bid',)

    def __unicode__(self):
        return "{} {} {} {} {}".format(
            self.player.id, self.player.name, self.team.manager.username,
            self.bid, self.get_status_display()
        )

    def set_new_highest(self):
        new_highest = TransferNomination.objects.filter(
            player=self.player
        ).exclude(status__in=[
            TransferNomination.ACCEPTED,
            TransferNomination.FAILED,
            TransferNomination.PASSED,
        ]).order_by('bid').first()
        if new_highest:
            new_highest.status = TransferNomination.HIGHEST
            new_highest.save()
            remaining_bids = TransferNomination.objects.filter(
                player=self.player, status=TransferNomination.OUTBID
            )
            for bid in remaining_bids:
                bid.status = TransferNomination.FAILED
                bid.save()

    @property
    def is_next_highest_bid(self):
        """Return True if status is outbid, but it's the highest of remaining bids."""
        remaining_bids = TransferNomination.objects.filter(
            player=self.player, status=TransferNomination.OUTBID
        ).order_by('-bid')

        return self == remaining_bids.first()

    def pass_on_bid(self):
        # # if this is the current highest then set the new highest first
        # if self.status == TransferNomination.HIGHEST:
        #     self.set_new_highest()
        self.status = TransferNomination.PASSED
        self.save()
        self.player.update_transfers()

    def accept_bid(self):
        from .functions import process_transfer_outcomes

        # bids can only be accepted if HIGHEST or LIST
        if self.status == TransferNomination.HIGHEST or self.status == TransferNomination.LIST:
            self.status = TransferNomination.ACCEPTED
            self.save()
            self.player.update_transfers()
            process_transfer_outcomes(self.team)
        else:
            print "ERROR: bid cannot be accepted"
            raise IllegalNominationOperationException('TransferNomination bid cannot be accepted.')

    def save(self, *args, **kwargs):
        """
        Ensure the nomination bid is at least the list price for the player.
        Extends the superclass method.
        """
        if self.bid < self.player.value:
            self.bid = self.player.value

        super(TransferNomination, self).save(*args, **kwargs)

        # TODO - put this in a signal?
        if self.status in [
                TransferNomination.HIGHEST,
                TransferNomination.LIST,
                TransferNomination.OUTBID,
                TransferNomination.FAILED
        ]:
            subject = "AZFF - Nomination update - {}".format(self.player)
            message = """
                      Hi {user},

                      Your nomination for {player} has been updated.
                      The status is now: {status}.

                      You can take any necessary action by visiting http://ffooty-dansapps.rhcloud.com/#/transfers

                      Good Luck

                      AZFF Admin
                      """
            body = message.format(
                user=self.team.manager.username,
                player=self.player,
                status=self.get_status_display(),
            )

            # try:
            #     send_mail(subject, body, 'noreply.azff@gmail.com', [self.team.manager.email], fail_silently=False)
            # except Exception, err:
            #     print "error sending mail: ", err


class SquadChange(models.Model):
    """
    Model for registering a squad/line-up change.
    """
    player = models.ForeignKey(Player)
    current_status = models.CharField(max_length=1, choices=Player.STATUS)
    new_status = models.CharField(max_length=1, choices=Player.STATUS)
    window = models.ForeignKey(Window)
    # the month the changes will take place
    week = models.ForeignKey(Week, null=True)
    processed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('player', 'window')

    def process(self):
        """
        Process the change.

        Only takes effect if the change has not been processed.
        Validation of the resulting line-up is the responsibility of the caller
        If validation fails `self.reverse()` should be used to undo the change.
        """
        if not self.processed:
            self.player.status = self.new_status
            self.processed = True
            self.player.save()
            print "{} processed from {} to {}.".format(
                self.player,
                self.get_current_status_display(),
                self.get_new_status_display(),
            )

    def reverse(self):
        """
        Reverse the change.

        Only takes effect if the change has been processed.
        """
        if self.processed:
            self.player.status = self.current_status
            self.processed = False
            self.player.save()
            print "{} reversed from {} to {}.".format(
                self.player,
                self.get_new_status_display(),
                self.get_current_status_display(),
            )


class Banter(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    text = models.TextField()

    class Meta:
        ordering = ['-added']

    def __unicode__(self):
        return self.text


class Comment(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    text = models.TextField()
    banter = models.ForeignKey(Banter, null=True, related_name='comments')

    def __unicode__(self):
        return self.text


class Constant(NameMixin):
    BOOLEAN = 'B'
    DATE = 'D'
    NUMBER = 'N'
    TEXT = 'T'

    TYPES = (
        (BOOLEAN, 'Boolean'),
        (DATE, 'Date'),
        (NUMBER, 'Number'),
        (TEXT, 'Text'),
    )

    type = models.CharField(max_length=1, choices=TYPES, default=NUMBER)
    description = models.TextField(null=True, blank=True)
    boolean_value = models.NullBooleanField(null=True, blank=True)
    date_value = models.DateField(null=True, blank=True)
    number_value = models.IntegerField(null=True, blank=True)
    text_value = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return '{} = {}'.format(self.name, self.value)

    @property
    def value(self):
        if self.type == self.NUMBER:
            return self.number_value
        elif self.type == self.TEXT:
            return self.text_value
        elif self.type == self.BOOLEAN:
            return self.bool_value
        elif self.type == self.DATE:
            return self.date_value
        else:
            return None
