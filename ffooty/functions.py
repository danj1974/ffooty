import csv
from datetime import datetime as dt, timedelta
import json
import random
import requests

from django.conf import settings
from django.db.models import Max

from ffooty.models import *


def initialise_weeks():
    """
    Create :class:``ffooty.models.Week`` objects for a season.

    :return: None
    """
    week_date = Constant.objects.get(name='START_DATE').value
    end_date = Constant.objects.get(name='END_DATE').value

    current_week = 1

    while week_date < end_date:
        Week.objects.create(number=current_week, date=week_date)
        current_week += 1
        week_date += timedelta(days=7)


def get_week():
    """
    Get the current Week instance.

    :return: the current Week or None if datetime.now() is before Week 1
    """
    now = dt.now().date()
    return Week.objects.filter(date__lte=now).order_by('-date').first()


def get_weeks_for_month(month=None):
    """
    Return the Week objects for a given month.

    The current month is used the ``month`` argument is not defined.

    :param int month: the month represented by an integer (1= Jan, etc)
    :return: a list of the weeks in the given month
    """
    if not month:
        month = dt.now().month
    return Week.objects.filter(date__month=month).order_by('number')


def get_current_window():
    """
    Returns the current active Window or None.
    """
    now = timezone.now()
    return Window.objects.filter(open_from__lte=now, deadline__gte=now).first()


def load_premiership_teams():
    """
    Load Premiership team data.
    TODO - extract to a fixture file or make admin page?
    """
    # list of PremTeams to add
    team_list = [
        {'name': 'Arsenal', 'code': 'ARS', 'is_prem': True, 'web_code': 3},
        {'name': 'Aston Villa', 'code': 'AVL', 'is_prem': True, 'web_code': 7},
        {'name': 'Bournemouth', 'code': 'BOU', 'is_prem': True, 'web_code': 91},
        {'name': 'Brentford', 'code': 'BRE', 'is_prem': True, 'web_code': 94},
        {'name': 'Brighton and Hove Albion', 'code': 'BTN', 'is_prem': True, 'web_code': 36},
        {'name': 'Burnley', 'code': 'BUR', 'is_prem': False, 'web_code': 90},
        {'name': 'Cardiff City', 'code': 'CAR', 'is_prem': False, 'web_code': None},
        {'name': 'Chelsea', 'code': 'CHE', 'is_prem': True, 'web_code': 8},
        {'name': 'Crystal Palace', 'code': 'CRY', 'is_prem': True, 'web_code': 31},
        {'name': 'Everton', 'code': 'EVE', 'is_prem': True, 'web_code': 11},
        {'name': 'Fulham', 'code': 'FUL', 'is_prem': True, 'web_code': 54},
        {'name': 'Hull', 'code': 'HUL', 'is_prem': False, 'web_code': None},
        {'name': 'Huddersfield Town', 'code': 'HUD', 'is_prem': False, 'web_code': None},
        {'name': 'Leeds United', 'code': 'LEE', 'is_prem': True, 'web_code': 2},
        {'name': 'Leicester City', 'code': 'LEI', 'is_prem': True, 'web_code': 13},
        {'name': 'Liverpool', 'code': 'LIV', 'is_prem': True, 'web_code': 14},
        {'name': 'Manchester City', 'code': 'MCY', 'is_prem': True, 'web_code': 43},
        {'name': 'Manchester United', 'code': 'MUN', 'is_prem': True, 'web_code': 1},
        {'name': 'Middlesbrough', 'code': 'MID', 'is_prem': False, 'web_code': None},
        {'name': 'Newcastle United', 'code': 'NEW', 'is_prem': True, 'web_code': 4},
        {'name': 'Norwich City', 'code': 'NOR', 'is_prem': False, 'web_code': 45},
        {'name': 'Nottingham Forest', 'code': 'NOT', 'is_prem': True, 'web_code': 17},
        {'name': 'Queens Park Rangers', 'code': 'QPR', 'is_prem': False, 'web_code': None},
        {'name': 'Sheffield United', 'code': 'SHF', 'is_prem': False, 'web_code': 49},
        {'name': 'Southampton', 'code': 'SOT', 'is_prem': True, 'web_code': 20},
        {'name': 'Stoke City', 'code': 'STO', 'is_prem': False, 'web_code': None},
        {'name': 'Sunderland', 'code': 'SUN', 'is_prem': False, 'web_code': None},
        {'name': 'Swansea City', 'code': 'SWA', 'is_prem': False, 'web_code': None},
        {'name': 'Tottenham Hotspur', 'code': 'TOT', 'is_prem': True, 'web_code': 6},
        {'name': 'Watford', 'code': 'WAT', 'is_prem': False, 'web_code': 57},
        {'name': 'West Bromwich Albion', 'code': 'WBA', 'is_prem': False, 'web_code': 35},
        {'name': 'West Ham United', 'code': 'WHM', 'is_prem': True, 'web_code': 21},
        {'name': 'Wolverhampton Wanderers', 'code': 'WLV', 'is_prem': True, 'web_code': 39},
    ]

    for team in team_list:
        print(PremTeam.objects.update_or_create(
            name=team['name'],
            code=team['code'],
            web_code=team['web_code'],
            defaults={'is_prem': team['is_prem']}
        ))
        # print(pt, created)


def get_prem_team_dict(key='code'):
    """
    Return a lookup dict of :class:``ffooty.models.PremTeam`` objects,

    Default key is 'code' but a

    :return: dict, key = ``code``, val = :class:``ffooty.models.PremTeam``
    """
    prem_team_dict = {}
    prem_teams = PremTeam.objects.all()
    for team in prem_teams:
        prem_team_dict[getattr(team, key)] = team
    return prem_team_dict


def get_team_dict():
    """
    Return a lookup dict of :class:``ffooty.models.PremTeam`` objects.

    :return: dict, key = manager username, val = :class:``ffooty.models.Team``
    """
    teams = Team.active_objects.all()
    return {t.manager.username: t for t in teams}


def get_player_codes():
    """
    Returns a dict of player positions and the latest code assigned.
    """
    return {
        Player.GKP: Player.objects.goalkeepers().aggregate(Max('code'))['code__max'] or 1000,
        Player.DEF: Player.objects.defenders().aggregate(Max('code'))['code__max'] or 2000,
        Player.MID: Player.objects.midfielders().aggregate(Max('code'))['code__max'] or 3000,
        Player.STR: Player.objects.strikers().aggregate(Max('code'))['code__max'] or 4000,
    }


def initialise_players(update=False, file_object=None):
    """
    Initialize player information from the TG website.

    This function should only be run once at the start of a season. If there
    are existing :class:``ffooty.models.Player`` records then the the method
    will not run.

    :return: None
    """
    # do not run if there are existing Player records
    players = Player.objects.all()
    if players.exists():
        # flag that this is an update performed to get new players before the auction
        update = True

    codes = get_player_codes()
    print("codes:", codes)

    # get a lookup dict of PremTeams, key = web_code
    prem_team_dict = get_prem_team_dict(key='web_code')
    print(prem_team_dict)

    # get the rows from the provided stats file
    if file_object:
        rows = json.load(file_object)
        file_object.close()
    else:
        print("No file object provided")
        return
    print("No. of player table rows = ", len(rows))

    # track new players *during update only*
    new_players = []

    print("****")
    print("New Players")
    print("****")

    for row in rows:

        first_name = row.get('first_name')
        if first_name:
            name = "{}. {}".format(first_name[0], row['last_name'])
        else:
            name = row['last_name']

        web_code = row['id']
        prem_team_code = row['squad_id']
        prem_team = prem_team_dict[prem_team_code]
        value = float(row['cost'] / 1000000.0)
        position = str(row['position'])

        # stats for new players can be an empty list
        stats = row['stats'] or {}

        last_years_total = stats.get('total_points', 0)

        # create (or update) a Player instance
        p, created = Player.objects.update_or_create(
            name=name, web_code=web_code,
            defaults={
                'prem_team': prem_team,
                'value': value,
                'last_years_total': last_years_total,
                'position': position,
            }
        )

        # assign the player codes if this is an update (i.e. pre-auction)
        if update and created:
            codes[p.position] += 1
            p.code = codes[p.position]
            p.is_new = True
            p.save()
            new_players.append(p)
            print(p.code, p.name, p.prem_team, p.value, created)

    print("****")
    print('All players saved')
    print("****")

    if not update:
        # Makes ure players are in the correct order before calculating tha AZFF player code
        # get each group of players (by position), order by decreasing value then
        # assign an incrementing code for AZFF
        # Note that we can't use the custom manager at this stage (it uses code not web_code)

        # GKP
        gkps = Player.objects.filter(position=Player.GKP).order_by('-value')
        print('gkps.count() = ', gkps.count())
        for g in gkps:
            codes[Player.GKP] += 1
            g.code = codes[Player.GKP]
            g.save()

        # DEF
        defs = Player.objects.filter(position=Player.DEF).order_by('-value')
        print('defs.count() = ', defs.count())
        for d in defs:
            codes[Player.DEF] += 1
            d.code = codes[Player.DEF]
            d.save()

        # MID
        mids = Player.objects.filter(position=Player.MID).order_by('-value')
        print('mids.count() = ', mids.count())
        for m in mids:
            codes[Player.MID] += 1
            m.code = codes[Player.MID]
            m.save()

        # STR
        strs = Player.objects.filter(position=Player.STR).order_by('-value')
        print('strs.count() = ', strs.count())
        for s in strs:
            codes[Player.STR] += 1
            s.code = codes[Player.STR]
            s.save()


def reset_for_new_season(definitely=False):
    if not definitely:
        print("Exiting - need to specify definitely=True (this is a rudimentary safeguard)")
        return

    archive_season_scores()

    players = Player.objects.all()
    for player in players:
        player.delete()

    weekly_scores = TeamWeeklyScore.objects.all()
    for tws in weekly_scores:
        tws.delete()

    monthly_scores = TeamMonthlyScore.objects.all()
    for tms in monthly_scores:
        tms.delete()

    total_scores = TeamTotalScore.objects.all()
    for tts in total_scores:
        tts.delete()

    transfer_noms = TransferNomination.objects.all()
    for nom in transfer_noms:
        nom.delete()

    auction_noms = AuctionNomination.objects.all()
    for nom in auction_noms:
        nom.delete()

    weeks = Week.objects.all()
    for week in weeks:
        week.delete()

    windows = Window.objects.all()
    for window in windows:
        window.delete()

    teams = Team.active_objects.all()
    for team in teams:
        team.score = 0
        team.funds = 0.0
        team.winnings = 0.0
        team.loss = 0.0
        team.cup_start_position = 0
        team.line_up_is_valid = False
        team.save()

    load_premiership_teams()
    initialise_weeks()


def update_players_json(week=None, file_object=None):
    # get a lookup dict of PremTeams, key = web_code
    prem_team_dict = get_prem_team_dict(key='web_code')

    if file_object:
        rows = json.load(file_object)
        file_object.close()
    else:
        rows = requests.get(settings.TG_PLAYERS_STATS_JSON).json()
    print("No. of player table rows = ", len(rows))

    # get the most recent codes assigned
    codes = get_player_codes()

    # get the round number for this week
    no_score_weeks = Constant.objects.get(name='NO_SCORE_WEEKS').value
    round_no = week.number - no_score_weeks

    # for each player in the main players table
    for row in rows:
        first_name = row.get('first_name')
        if first_name:
            name = "{}. {}".format(first_name[0], row['last_name'])
        else:
            name = row['last_name']

        web_code = row['id']

        # get existing player (or None if the web code isn't in the db)
        player = Player.objects.filter(web_code=web_code).first()

        if row["status"] == "eliminated":
            if player.is_active:
                print("{}: {} is now inactive".format(
                    player.code, name
                ))
                player.is_active = False
                player.save()

            continue

        prem_team_code = row['squad_id']
        prem_team = prem_team_dict[prem_team_code]
        value = float(row['cost'] / 1000000.0)
        position = str(row['position'])

        # stats for new players can be an empty list
        stats = row['stats'] or {}

        total_score = stats.get('total_points', 0)
        round_scores = stats.get('round_scores')
        appearances = stats.get('games_played', 0)

        # `round_scores` is a dict if populated, e.g. {'1': 2, '2': 19} where the key
        # is the week number, but if empty is an empty list
        if not round_scores:
            week_score = None
        else:
            week_score = round_scores.get(str(round_no))

        if player:
            # if team has changed, flag player as 'new' and update the team
            if str(player.prem_team) != str(prem_team):
                print("{}: team change from {} to {}".format(
                    player.code, player.prem_team, prem_team
                ))
                # TODO - review when to make is_new = false
                player.is_new = True
                player.prem_team = prem_team

            player.appearances = appearances
            player.total_score = total_score
            player.save()
        else:
            codes[position] += 1
            player_code = codes[position]

            player = Player.objects.create(
                name=name,
                position=position,
                code=player_code,
                web_code=web_code,
                prem_team=prem_team,
                value=value,
                total_score=total_score,
                is_new=True,
                appearances=appearances,
            )

            print("New Player: {}: {} {}, {}".format(
                player.code, player.name, player.prem_team, player.value
            ))

        # create a new PlayerScore if it's a scoring week and the player is owned by a team
        # TODO - currently creating PlayerScores for all players - mainly used to identify inactive players
        if week:
            PlayerScore.objects.update_or_create(
                player=player,
                week=week,
                team=player.team,
                defaults={'value': week_score}
            )

    # TODO - is this still needed??
    if week:
        # find any players without a PlayerScore this week and deactivate them
        players = Player.objects.filter(is_active=True)
        for p in players:
            week_score = PlayerScore.objects.filter(week=week, player=p).first()
            if week_score is None:
                p.is_active = False
                p.save()


def update_weekly_scores(week):
    teams = Team.active_objects.all()

    for team in teams:

        # flags to count reserve player scores:
        include_reserve = {
            Player.GKP: False,
            Player.DEF: False,
            Player.MID: False,
            Player.STR: False
        }

        week_score = 0

        # get team players and order by status (first team > reserve > squad)
        for player in team.players.order_by('status'):
            print("player = ", player)
            score = PlayerScore.objects.filter(player=player, week=week).first()

            if score and score.value is not None:
                # determine if the score counts
                if player.status == Player.FIRST_TEAM or \
                        (player.status == Player.RESERVE and include_reserve[player.position]):
                    # add the score to the total
                    week_score += score.value
                    score.is_counted = True
                    score.save()
                    print("score for {} ({}) is {}, counted = {}".format(
                        player.name, player.status, score.value, score.is_counted
                    ))

            else:
                # if it's a first team player, we flag that the reserve score can be counted
                if player.status == Player.FIRST_TEAM:
                    include_reserve[player.position] = True

            # get or create the PlayerTeamScore for this team & player and update its value
            player_team_score, _created = PlayerTeamScore.objects.get_or_create(
                player=player, team=team
            )
            player_team_score.update()

        # update or create the weekly score for the team
        TeamWeeklyScore.objects.update_or_create(team=team, week=week,
                                                 defaults={'value': week_score})

        # get or create the TeamMonthlyScore and update it
        monthly_score, _created = TeamMonthlyScore.objects.get_or_create(
            team=team, month=week.date.month)
        monthly_score.update()

        # and finally update the total score for the team
        team.update_total_score()


def update_no_score_week(week=None):
    if week:
        players = Player.objects.select_related('team')
        for p in players:
            PlayerScore.objects.create(player=p, team=p.team, week=week, value=None)

        # update the constant monitoring the number of 'no score' weeks
        c = Constant.objects.get(name="NO_SCORE_WEEKS")
        c.number_value += 1
        c.save()


def get_weeks_and_scores_for_month(team, month=None):
    weeks = get_weeks_for_month(month)

    # TODO - change to team=team but need to take care of historical data
    player_scores = PlayerScore.objects.filter(team=team, week__in=weeks)
    weekly_scores = TeamWeeklyScore.objects.filter(team=team, week__in=weeks)

    return weeks, player_scores, weekly_scores


def export_player_sales():
    """
    Export a csv file of players who have been bought during auction..
    """
    # get players belonging to a team
    players = Player.objects.filter(team__isnull=False)

    with open('/home/dan/Documents/ffooty_data/csv_exports/player_sales_auction.csv', 'wb') as f:
        writer = csv.writer(f)

        for p in players:
            writer.writerow([p.code, p.team.id, p.sale])


def export_player_list_csv():
    """
    Export a csv file of all players.
    """
    # get players belonging to a team
    players = Player.objects.select_related(
        'team', 'team__manager'
    ).order_by(
        '-value', 'code'
    )

    with open('./data/player_list_auction.csv', 'w') as f:
        writer = csv.writer(f)

        for position in Player.POSITION:

            writer.writerow([
                'Code',	'Name',	'Team',	'Value', 'Pts', 'Manager', 'Manager Nominations'
            ])

            for p in players.filter(position=position[0]):
                writer.writerow([
                    p.code,
                    p.name,
                    p.prem_team.code,
                    p.value,
                    p.last_years_total,
                    p.team.manager.username if p.team else '',
                    p.auction_nomination_managers
                ])


def process_transfer_nominations():
    players = TransferNomination.objects.select_related(
        'player').values_list('player_id', flat=True)
        #'player').values('player_id').distinct('player')  # distinct not support by sqlite3

    player_ids = list(set(players))

    for id in player_ids:
        player = Player.objects.get(id=id)
        print("Updating transfer for ", player.name)
        player.update_transfers()


def process_transfer_outcomes(team):
    """
    Process TransferNomination outcomes for a window.
    """
    tns = TransferNomination.objects.filter(
        team=team, processed=False
    ).select_related('player', 'team', 'team__manager')
    messages = []

    week = get_week()

    for tn in tns:
        if tn.status in [TransferNomination.PENDING, TransferNomination.HIGHEST,
                         TransferNomination.LIST, TransferNomination.OUTBID]:
            continue  # don't set the processed flag
        elif tn.status in [TransferNomination.PASSED, TransferNomination.FAILED]:
            # tn.delete()
            pass
        elif tn.status == TransferNomination.ACCEPTED:
            tn.player.team = tn.team
            tn.player.sale = tn.bid    # LIST outcomes have already set bid to list value
            tn.player.save()
            messages.append("Adding {} to {}'s team (sale = {})".format(
                tn.player.name, tn.player.team.manager.username, tn.player.sale
            ))
            # add a dummy player score record so new players show in team pages
            PlayerScore.objects.create(
                player=tn.player,
                team=team,
                value=None,
                week=week,
            )
            PlayerTeamScore.objects.get_or_create(
                player=tn.player,
                team=team,
                defaults={'value': 0}
            )
        else:
            messages.append("Error processing nomination: {}".format(tn))
            continue
        tn.processed = True
        tn.save()

    team.update_funds()

    return messages


def get_months_to_date():
    """
    Return a list of months (as ints) current month first to the start of the season.
    """
    month_sequence = [5, 4, 3, 2, 1, 12, 11, 10, 9, 8]  # season is August to May
    try:
        current_month_index = month_sequence.index(dt.now().month)
    except ValueError:
        current_month_index = 0

    return month_sequence[current_month_index:]


def month_is_complete(month):
    """
    Return True if today's date is on or after the last score week of a month.
    :param month: the month to check as int
    :return: bool
    """
    today = dt.today().date()
    # get the weeks for the month
    weeks = get_weeks_for_month(month)
    # compare todays date to the last week in the month
    return today >= weeks.latest('date').date


def award_motm(month):
    """
    Award the Manager of the Month prize for the given month.

    :param month: the month as an integer (Jan = 1, etc)
    :return: the high-scoring :class:`ffooty.models.TeamMonthlyScore`
    instance or None if the month is not yet complete.
    """
    if not month_is_complete(month):
        print("Month {} is not complete!".format(month))
        return None

    # get the scores for the month in descending order
    scores = TeamMonthlyScore.objects.filter(
        month=month
    ).select_related(
        'team', 'team__manager'
    ).order_by('-value')

    awarded = scores.filter(prize_awarded=True).first()  # there should only be 1 per month
    print("awarded = ", awarded)
    highest = scores[0]
    print("highest = ", highest)

    if awarded and awarded == highest:
        print("confirmed: MOTM for {} awarded: {}".format(month, awarded))
        return awarded
    elif awarded:
        # reset the current winner
        awarded.prize_awarded = False
        awarded.save()
        # deduct the winnings
        awarded.team.process_motm(win=False)

    # set the new winner
    highest.prize_awarded = True
    highest.save()
    highest.team.process_motm()
    return highest


def initialise_cup_competition(bye_list=[]):
    """
    Initialise the starting positions for the cup competition.

    Assigns each team a number from 1 - 16 to begin a 4-round knockout cup
    competition.  In the first round teams play as follows: 1 vs 2, 2 vs 3,
    ...., 15 vs 16. Then winners of 1 - 4 play each other in quarter final
    (and 5 - 8, etc.). Then semis from 1 - 8 and 9 - 16.  You get the picture.

    If the number of teams is less than 16 (typically 12-14 teams in a league)
    then a list of Teams can be provided who will have a bye in the first round.

    :param bye_list: list of teams
    :return:
    """
    # create a list of all teams
    teams = list(Team.active_objects.all())

    # if no. of teams + no. of byes is less than 16 then one or more random byes are required
    random_byes = 16 - len(teams) - len(bye_list)

    # if it's more than then there's a problem
    # TODO - raise an error here
    if random_byes < 0:
        print(len(teams), len(bye_list))
        print("Error: teams + byes > 16")
        exit

    # add a None for each random bye to be incorporated into the random list
    for i in range(random_byes):
        print(" adding random bye")
        teams.append(None)

    # randomise the list
    random.shuffle(teams)

    print("randomised teams:")
    print(teams)

    # flag for monitoring when planned byes are needed
    bye_next = False
    # flag for monitoring byes assigned in previous step
    bye_previous = False

    for position in range(1, 17):

        # pass over the position when a bye is required
        if bye_next:
            bye_next = False
            continue

        # get the next team from the randomised list
        team = teams.pop()

        # pass over any Nones in the list and set the previous flag
        if not team and not bye_previous:
            print("if not team and not bye_previous")
            bye_previous = True
            continue
        elif not team:
            print("elif not team")
            # add the team/None back to the list and reshuffle until the next one is note none
            teams.append(team)
            while teams[-1] is not None:
                print("Two Nones in a row - shuffling")
                random.shuffle(teams)
            team = teams.pop()

        # deal with planned byes
        if team in bye_list:
            # if the position is an even number we can only assign the position if the bye_previous flag is set
            if position % 2 == 0:
                if bye_previous:
                    team.cup_start_position = position
                    # in which case we need to add the a bye back to the list to replace the random one
                    teams.append(None)
                else:
                    # otherwise we need to re-add the team back to the end of the list and pop the next non-bye team
                    index = -1
                    while len(teams) + index >= 0:
                        print("executing while loop: index = ", index)
                        if teams[index] is not None and teams[index] not in bye_list:
                            old_team = team
                            team = teams.pop(index)
                            teams.append(old_team)
                            break
                        index -= 1
                    team.cup_start_position = position
            else:
                team.cup_start_position = position
                bye_next = True
        else:
            # simply assign the team to the current position
            team.cup_start_position = position

        # finally save the team and set previous flag back to False
        team.save()
        bye_previous = False


def get_cup_scores():
    cup_weeks = Week.objects.filter(is_cup=True)
    teams = Team.active_objects.all().order_by('cup_start_position')
    current_week = get_week()

    assert cup_weeks.count() == 4, "There should be 4 cup weeks assigned."

    # process round 1
    positions = []
    for position in range(1, 17):
        team = teams.filter(cup_start_position=position).first()  # sets to None if no team found
        positions.append(team)

    # slice the list into odds and evens then pair them up
    round_pairs = zip(positions[0::2], positions[1::2])

    for pair in round_pairs:
        pass


def archive_season_scores():
    """
    Archive each team's score for the season.

    Create :class:`ffooty.models.TeamTotalScoreArchive` instances for each team.
    :return:
    """
    teams = Team.active_objects.all()
    year = dt.now().year - 1

    print("archiving year {} for {} teams".format(year, teams.count()))

    for team in teams:
        print("{} scored {} in {}".format(team, team.score, year))

        print(TeamTotalScoreArchive.objects.update_or_create(
            team=team,
            year=year,
            defaults={'value': team.score}
        ))


class SquadChangeException(Exception):
    pass


def process_squad_changes(team, window, validate_only=True):
    """
    Process the stored `SquadChange` records for a given Team and Window.

    Return a boolean indicating whether the processing was successful (i.e.
    that a valid team line up was obtained). If the `validate_only` flag is
    set then reverse the processing to leave the team unchanged.

    :param team: the :class:`ffooty.models.Team` to check
    :param window: the :class:`ffooty.models.Window` to validate
    :param bool validate_only: flag to indicate
    :return: bool
    """
    changes = SquadChange.objects.select_related(
        'player', 'player__team'
    ).filter(player__team=team, window=window)

    for change in changes:
        change.process()

    is_valid = team.validate_line_up()

    # reverse the process if the line up is not valid (or the validate_only flag is raised)
    if not is_valid or validate_only:
        for change in changes:
            change.reverse()

    # if team.validate_line_up():
    #     message = 'Squad changes for {} could not be reversed'.format(team)
    #     raise SquadChangeException()

    return is_valid
