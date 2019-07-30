# from dateutil.parser import parse as dateParse

import csv
from datetime import datetime as dt, timedelta
from decimal import Decimal
import json
import os
import random
import requests
import socket
import urllib2
from urllib import urlopen
from xlrd import open_workbook

import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common import utils
from selenium.webdriver.phantomjs.service import Service

from django.conf import settings
from django.db.models import Max

from ffooty.models import *


def initialise_weeks():
    """
    Create :class:``ffooty.mpdels.Week`` objects for a season.

    :return: None
    """
    # TODO - use the constants to set the start/end date
    # TODO - or submit dates in the form when uploading the players.
    week_date = dt(2019, 8, 13)  # the first Tuesday after start of season
    end_date = dt(2020, 5, 27)  # the *Wednesday* after the cup final/last weekend

    current_week = 1

    while week_date < end_date:
        w = Week.objects.create(number=current_week, date=week_date)
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


def load_premiership_teams():
    """
    Load Premiership team data.
    TODO - extract to a fixture file or make admin page?
    """
    # list of PremTeams to add
    team_list = [
        {'name': 'Arsenal', 'code': 'ARS', 'is_prem': True},
        {'name': 'Aston Villa', 'code': 'AVL', 'is_prem': True},
        {'name': 'Brighton', 'code': 'BTN', 'is_prem': True},
        {'name': 'Bournemouth', 'code': 'BOU', 'is_prem': True},
        {'name': 'Burnley', 'code': 'BUR', 'is_prem': True},
        {'name': 'Cardiff City', 'code': 'CAR', 'is_prem': False},
        {'name': 'Chelsea', 'code': 'CHE', 'is_prem': True},
        {'name': 'Crystal Palace', 'code': 'CRY', 'is_prem': True},
        {'name': 'Everton', 'code': 'EVE', 'is_prem': True},
        {'name': 'Fulham', 'code': 'FUL', 'is_prem': False},
        {'name': 'Hull', 'code': 'HUL', 'is_prem': False},
        {'name': 'Huddersfield Town', 'code': 'HUD', 'is_prem': False},
        {'name': 'Leicester City', 'code': 'LEI', 'is_prem': True},
        {'name': 'Liverpool', 'code': 'LIV', 'is_prem': True},
        {'name': 'Manchester City', 'code': 'MCY', 'is_prem': True},
        {'name': 'Manchester United', 'code': 'MUN', 'is_prem': True},
        {'name': 'Middlesbrough', 'code': 'MID', 'is_prem': False},
        {'name': 'Newcastle United', 'code': 'NEW', 'is_prem': True},
        {'name': 'Norwich City', 'code': 'NOR', 'is_prem': True},
        {'name': 'Queens Park Rangers', 'code': 'QPR', 'is_prem': False},
        {'name': 'Sheffield United', 'code': 'SHF', 'is_prem': True},
        {'name': 'Southampton', 'code': 'SOT', 'is_prem': True},
        {'name': 'Stoke City', 'code': 'STO', 'is_prem': False},
        {'name': 'Sunderland', 'code': 'SUN', 'is_prem': False},
        {'name': 'Swansea City', 'code': 'SWA', 'is_prem': False},
        {'name': 'Tottenham Hotspur', 'code': 'TOT', 'is_prem': True},
        {'name': 'Watford', 'code': 'WAT', 'is_prem': True},
        {'name': 'West Bromwich Albion', 'code': 'WBA', 'is_prem': False},
        {'name': 'West Ham United', 'code': 'WHM', 'is_prem': True},
        {'name': 'Wolverhampton Wanderers', 'code': 'WLV', 'is_prem': True},
    ]

    for team in team_list:
        print PremTeam.objects.update_or_create(
            name=team['name'],
            code=team['code'],
            defaults={'is_prem': team['is_prem']}
        )
        # print pt, created


def is_player_stats_table_visible(session):
    print "waiting for playerstats to load..."
    players_source = BeautifulSoup(session.body())
    rows = players_source.findAll('tr', {'class': 'playerstats'})
    if rows:
        return True
    else:
        return False


def new_free_port():
    """
    Determines a free port using sockets.
    """
    ip = os.environ['OPENSHIFT_PYTHON_IP']
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind((ip, 0))
    free_socket.listen(5)
    port = free_socket.getsockname()[1]
    free_socket.close()
    return port


class NewService(Service):

    def __init__(self, executable_path, port=0, service_args=None, log_path=None):
        self.port = '127.8.247.1:8080'
        self.path = executable_path
        self.service_args= service_args
        if self.port == 0:
            self.port = new_free_port()
        if self.service_args is None:
            self.service_args = []
        else:
            self.service_args=service_args[:]
        self.service_args.insert(0, self.path)
        self.service_args.append("--webdriver=%d" % self.port)
        if not log_path:
            log_path = "ghostdriver.log"
        self._log = open(log_path, 'w')


def get_player_rows():
    """
    Return an iterable containing ``<tr>`` elements from TG player list.

    :return: iterable containing :class:``bs4.element.Tag`` of player data.
    :rtype: :class:``bs4.element.ResultSet``
    """
    # players_source = BeautifulSoup(urlopen(settings.TG_PLAYERS_STATS))

    if settings.ON_OPENSHIFT:
        webdriver.phantomjs.webdriver.Service = NewService

    print "settings.ON_OPENSHIFT:", settings.ON_OPENSHIFT
    print "settings.PHANTOMJS_PATH: ", settings.PHANTOMJS_PATH

    browser = webdriver.PhantomJS(settings.PHANTOMJS_PATH)
    browser.get(settings.TG_PLAYERS_STATS)

    players_source = BeautifulSoup(browser.page_source, "html.parser")
    player_table = players_source.find(id="table-players")
    return player_table.findAll('tr', {'class': 'playerstats'})


def get_player_rows_from_file(file_object=None, initialise=False):
    if not file_object:
        file_object = open('/home/dan/ffooty/website_data/player_table.html')
    players_source = BeautifulSoup(file_object)

    # when initialising the table pre-season, different table id & row classes are needed
    # stats centre table is valid pre-season 2019
    # if initialise:
    #     table_id = 'player-selection-list'
    #     row_class = 'accel'
    # else:
    #     table_id = 'table-players'
    #     row_class = 'playerstats'

    table_id = 'table-players'
    row_class = 'playerstats'

    player_table = players_source.find(id=table_id)
    return player_table.findAll('tr', {'class': row_class})


def get_prem_team_dict():
    """
    Return a lookup dict of :class:``ffooty.models.PremTeam`` objects,

    :return: dict, key = ``code``, val = :class:``ffooty.models.PremTeam``
    """
    prem_team_dict = {}
    prem_teams = PremTeam.objects.all()
    for team in prem_teams:
        prem_team_dict[team.code] = team
    return prem_team_dict


def get_team_dict():
    """
    Return a lookup dict of :class:``ffooty.models.PremTeam`` objects.

    :return: dict, key = manager username, val = :class:``ffooty.models.Team``
    """
    teams = Team.active_objects.all()
    return {t.manager.username: t for t in teams}


def get_player_codes():
    codes = {
        'G': Player.objects.goalkeepers().aggregate(Max('code'))['code__max'],
        'D': Player.objects.defenders().aggregate(Max('code'))['code__max'],
        'M': Player.objects.midfielders().aggregate(Max('code'))['code__max'],
        'S': Player.objects.strikers().aggregate(Max('code'))['code__max']
    }

    return codes


def initialise_players(update=False, from_file=True, file_object=None):
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
        print codes
    else:
        codes = {
            'G': 1000,
            'D': 2000,
            'M': 3000,
            'S': 4000,
        }

    print "codes:", codes

    # get a lookup dict of PremTeams, key = name
    prem_team_dict = get_prem_team_dict()
    print prem_team_dict

    # get the rows from the provided stats file, or request it directly
    if file_object:
        rows = json.loads(file_object.read())['playerstats']
        file_object.close()
    else:
        rows = requests.get(settings.TG_PLAYERS_STATS_JSON).json()['playerstats']
    print "No. of player table rows = ", len(rows)

    # track new players *during update only*
    new_players = []

    print "****"
    print "New Players"
    print "****"

    for row in rows:
        name = row['PLAYERNAME']
        web_code = row['PLAYERID']
        prem_team_code = row['TEAMCODE']
        prem_team = prem_team_dict[prem_team_code]
        value = float(row['VALUE'])

        try:
            last_years_total = int(row['POINTS'])
        except (KeyError, ValueError):
            # no points available for previous season
            last_years_total = 0

        # create (or update) a Player instance
        p, created = Player.objects.update_or_create(
            name=name, web_code=web_code,
            defaults={
                'prem_team': prem_team,
                'value': value,
                'last_years_total': last_years_total
            }
        )

        # assign the player codes if this is an update (i.e. pre-auction)
        if update and created:
            codes[p.position] += 1
            p.code = codes[p.position]
            p.is_new = True
            p.save()
            new_players.append(p)
            print p.code, p.name, p.prem_team, p.value, created

    print "****"
    print 'All players saved'
    print "****"

    if not update:
        # Makes ure players are in the correct order before calculating tha AZFF player code
        # get each group of players (by position), order by decreasing value then
        # assign an incrementing code for AZFF
        # Note that we can't use the custom manager at this stage (it uses code not web_code)

        # GKP
        gkps = Player.objects.filter(web_code__lt=2000).order_by('-value')
        print 'gkps.count() = ', gkps.count()
        for g in gkps:
            codes['G'] += 1
            g.code = codes['G']
            g.save()

        # DEF
        defs = Player.objects.filter(web_code__range=(2000, 2999)).order_by('-value')
        print 'defs.count() = ', defs.count()
        for d in defs:
            codes['D'] += 1
            d.code = codes['D']
            d.save()

        # MID
        mids = Player.objects.filter(web_code__range=(3000, 3999)).order_by('-value')
        print 'mids.count() = ', mids.count()
        for m in mids:
            codes['M'] += 1
            m.code = codes['M']
            m.save()

        # STR
        strs = Player.objects.filter(web_code__gte=4000).order_by('-value')
        print 'strs.count() = ', strs.count()
        for s in strs:
            codes['S'] += 1
            s.code = codes['S']
            s.save()


def reset_for_new_season(definitely=False):
    if not definitely:
        print "Exiting - need to specify definitely=True (this is a rudimentary safeguard)"
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


def update_players(week=None, from_file=False, file_object=None):
    # get a lookup dict of PremTeams, key = name
    prem_team_dict = get_prem_team_dict()

    # get the rows from the players table
    if from_file:
        rows = get_player_rows_from_file(file_object=file_object)
    else:
        rows = get_player_rows()
    print "No. of player table rows = ", len(rows)

    # get the most recent codes assigned
    codes = get_player_codes()

    # for each <tr> element in the main players table
    for row in rows:
        attrs = row.attrs

        if 'table-head' in attrs['class']:
            continue

        # if attrs['data-status'] == 'HIDDEN':
        #     continue

        # first cell contains <a href"player-stat-address"><img>player-name</img></a>
        name = attrs['data-name']
        web_code = attrs['data-playerid']
        prem_team_code = attrs['data-team']
        prem_team = prem_team_dict[prem_team_code]
        value = float(attrs['data-value'])
        try:
            total_score = int(attrs['data-points'])
            week_score = int(attrs['data-weekpoints'])
        except ValueError:
            # no points available
            total_score = 0
            week_score = 0

        # get existing player (or None if the web code isn't in the db)
        player = Player.objects.filter(web_code=web_code).first()

        if player:
            # check the weekly and total scores against the existing total
            if total_score != week_score + player.total_score:
                print "ERROR: Points don't add up for player ", player
                print "Web player total = {}, but week_score = {} and current total = {}".format(
                    total_score, week_score, player.total_score
                )
            # if team has changed, flag player as 'new' and update the team
            if str(player.prem_team) != str(prem_team):
                print "{}: {}; team change from {} to {}".format(player.code,
                                                                 name,
                                                                 player.prem_team,
                                                                 prem_team)
                # TODO - review when to make is_new = false
                player.is_new = True
                player.prem_team = prem_team
                player.save()

        else:
            player = Player.objects.create(name=name, web_code=web_code,
                                           prem_team=prem_team, value=value)
            codes[player.position] += 1
            player.code = codes[player.position]
            player.is_new = True

            print "New Player: {}: {}, {}, {}".format(player.code, player.name, player.prem_team, player.value)

        # compare appearance totals with database to determine if player played.
        starts = row.find('td', {'class': 'player-sxi'}).text
        subs = row.find('td', {'class': 'player-subs'}).text
        new_appearances = int(starts) + int(subs)

        if new_appearances <= player.appearances:
            if week_score == 0:
                week_score = None
            else:
                print "ERROR: appearances for player: ", player
                print "week_score = {}, but new_appearances = {} and current appearances = {}".format(
                    week_score, new_appearances, player.appearances
                )

        player.total_score = total_score
        player.appearances = new_appearances
        player.save()

        # create a new PlayerScore if it's a scoring week and the player is owned by a team
        # TODO - currently creating PlayerScores for all players - mainly used to identify inactive players

        if week:
            PlayerScore.objects.update_or_create(player=player, week=week, team=player.team,
                                                 defaults={'value': week_score})

    # find any players without a PlayerScore this week and deactivate them
    players = Player.objects.filter(is_active=True)
    for p in players:
        week_score = PlayerScore.objects.filter(week=week, player=p).first()
        if week_score is None:
            p.is_active = False
            p.save()


def update_players_json(week=None, from_file=False, file_object=None):
    # get a lookup dict of PremTeams, key = name
    prem_team_dict = get_prem_team_dict()

    if file_object:
        rows = json.loads(file_object.read())['playerstats']
        file_object.close()
    else:
        rows = requests.get(settings.TG_PLAYERS_STATS_JSON).json()['playerstats']
    print "No. of player table rows = ", len(rows)

    # get the most recent codes assigned
    codes = get_player_codes()

    # for each player in the main players table
    for row in rows:

        name = row['PLAYERNAME']
        web_code = row['PLAYERID']
        prem_team_code = row['TEAMCODE']
        prem_team = prem_team_dict[prem_team_code]
        value = float(row['VALUE'])
        try:
            total_score = int(row['POINTS'])
            week_score = int(row['WEEKPOINTS'])
        except ValueError:
            # no points available
            total_score = 0
            week_score = 0

        # get existing player (or None if the web code isn't in the db)
        player = Player.objects.filter(web_code=web_code).first()
        
        if player:
            # check the weekly and total scores against the existing total
            if total_score != week_score + player.total_score:
                print "ERROR: Points don't add up for player ", player
                print "Web player total = {}, but week_score = {} and current total = {}".format(
                    total_score, week_score, player.total_score
                )
            # if team has changed, flag player as 'new' and update the team
            if str(player.prem_team) != str(prem_team):
                print "{}: {}; team change from {} to {}".format(player.code,
                                                                 name,
                                                                 player.prem_team,
                                                                 prem_team)
                # TODO - review when to make is_new = false
                player.is_new = True
                player.prem_team = prem_team
                player.save()
        else:
            player = Player.objects.create(name=name, web_code=web_code,
                                           prem_team=prem_team, value=value)
            codes[player.position] += 1
            player.code = codes[player.position]
            player.is_new = True

            print "New Player: {}: {}, {}, {}".format(player.code, player.name, player.prem_team, player.value)

        # compare appearance totals with database to determine if player played.
        starts = row['SXI']
        subs = row['SUBS']
        new_appearances = starts + subs

        if new_appearances <= player.appearances:
            if week_score == 0:
                week_score = None
            else:
                print "ERROR: appearances for player: ", player
                print "week_score = {}, but new_appearances = {} and current appearances = {}".format(
                    week_score, new_appearances, player.appearances
                )
        player.total_score = total_score
        player.appearances = new_appearances
        player.save()

        # create a new PlayerScore if it's a scoring week and the player is owned by a team
        # TODO - currently creating PlayerScores for all players - mainly used to identify inactive players
        if week:
            PlayerScore.objects.update_or_create(player=player, week=week, team=player.team,
                                                 defaults={'value': week_score})


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
            'G': False,
            'D': False,
            'M': False,
            'S': False
        }

        week_score = 0

        # get team players and order by status (first team > reserve > squad)
        for player in team.players.order_by('status'):
            print "player = ", player
            score = PlayerScore.objects.filter(player=player, week=week).first()

            if score.value is not None:
                # determine if the score counts
                if player.status == Player.FIRST_TEAM or \
                        (player.status == Player.RESERVE and include_reserve[player.position]):
                    # add the score to the total
                    week_score += score.value
                    score.is_counted = True
                    score.save()
                    print "score for {} ({}) is {}, counted = {}".format(player.name, player.status, score.value, score.is_counted)

            elif score.value is None:
                # if it's a first team player, we flag that the reserve score can be counted
                if player.status == Player.FIRST_TEAM:
                    include_reserve[player.position] = True

            else:
                print "****ERROR****: Logic needs reviewing:"
                print "Player:", player, "score:", score

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


def player_has_played(web_code, week):

    # get the individual player stats (<tr> elements)
    player_source = BeautifulSoup(urlopen(settings.TG_PLAYER_STATS_BASE + str(web_code)))
    player_stats = player_source.find_all("tr")

    for row in player_stats:
        if row.contents[1].string == 'Week':
            # ignore the header row
            continue
        elif row.contents[1].string == 'Vs':
            # unrecognised player code
            return False
        # get the week for the row
        stat_week = int(row.contents[1].string)
        if stat_week == week:
            # entry for this week found
            return True
        elif stat_week > week:
            # entry for a later week found
            continue
        else:
            # entry for this week not found
            return False
    # finally for players with no table entry in their stats page:
    return False


def get_player_score(web_code, week):
    # get the individual player stats (<tr> elements)
    player_source = BeautifulSoup(urlopen(settings.TG_PLAYER_STATS_BASE + str(web_code)))
    player_stats = player_source.find_all("tr")

    score = 0

    for row in player_stats:
        if row.contents[1].string == 'Week':
            # ignore the header row
            continue
        elif row.contents[1].string == 'Vs':
            # unrecognised player code
            return None
        # get the week for the row
        stat_week = int(row.contents[1].string)
        if stat_week > week:
            continue
        elif stat_week == week:
            score += int(row.contents[-2].string)
            continue
        else:  # stat_week < week
            break

    return score


def update_no_score_week(week=None):
    if week:
        players = Player.objects.select_related('team')
        for p in players:
            PlayerScore.objects.create(player=p, team=p.team, week=week, value=None)


def get_weeks_and_scores_for_month(team, month=None):
    weeks = get_weeks_for_month(month)

    # TODO - change to team=team but need to take care of historical data
    player_scores = PlayerScore.objects.filter(team=team, week__in=weeks)
    weekly_scores = TeamWeeklyScore.objects.filter(team=team, week__in=weeks)

    return weeks, player_scores, weekly_scores


def read_auction_excel_file(filepath):
    """
    Read in an Excel file with details of auction sales.

    Column 0 [A]: player code
    Column 4 [E]: Manager
    Column 5 [F]: sale
    """
    # create a lookup dict of teams by manager name
    teams = Team.active_objects.all()
    team_dict = {}

    for t in teams:
        team_dict[t.manager.username] = t

    wb = open_workbook(filepath)
    s = wb.sheet_by_index(0)

    for rw in range(s.nrows):
        if s.cell_value(rw, 4) not in ['', 'Manager']:
            player = Player.objects.get(code=int(s.cell_value(rw, 0)))
            player.team = team_dict[s.cell_value(rw, 4)]
            player.sale = float(s.cell_value(rw, 5))
            player.save()


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
        print "Updating transfer for ", player.name
        player.update_transfers()


def process_transfer_outcomes(team):
    """
    Process TransferNomination outcomes for a window.
    """
    tns = TransferNomination.objects.filter(
        team=team, processed=False
    ).select_related('player', 'team', 'team__manager')
    messages = []

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
        print "Month {} is not complete!".format(month)
        return None

    # get the scores for the month in descending order
    scores = TeamMonthlyScore.objects.filter(
        month=month
    ).select_related(
        'team', 'team__manager'
    ).order_by('-value')

    awarded = scores.filter(prize_awarded=True).first()  # there should only be 1 per month
    print "awarded = ", awarded
    highest = scores[0]
    print "highest = ", highest

    if awarded and awarded == highest:
        print "confirmed: MOTM for {} awarded: {}".format(month, awarded)
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
        print len(teams), len(bye_list)
        print "Error: teams + byes > 16"
        exit

    # add a None for each random bye to be incorporated into the random list
    for i in range(random_byes):
        print " adding random bye"
        teams.append(None)

    # randomise the list
    random.shuffle(teams)

    print "randomised teams:"
    print teams

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
            print "if not team and not bye_previous"
            bye_previous = True
            continue
        elif not team:
            print "elif not team"
            # add the team/None back to the list and reshuffle until the next one is note none
            teams.append(team)
            while teams[-1] is not None:
                print "Two Nones in a row - shuffling"
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
                        print "executing while loop: index = ", index
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

    print "archiving year {} for {} teams".format(year, teams.count())

    for team in teams:
        print "{} scored {} in {}".format(team, team.score, year)

        print TeamTotalScoreArchive.objects.update_or_create(
            team=team,
            year=year,
            defaults={'value': team.score}
        )


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
