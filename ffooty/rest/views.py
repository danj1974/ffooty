import random

from calendar import month_name
from datetime import date

from django.db.models import Count
from django.utils import timezone
from rest_framework import status
# from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from ffooty.functions import (get_weeks_and_scores_for_month, get_week, update_weekly_scores,
                              process_transfer_outcomes, get_months_to_date, get_current_window)
from ffooty.models import (Constant, Team, AuctionNomination, Player, Window, TeamMonthlyScore,
                           TransferNomination, PlayerTeamScore, )
from ffooty.rest.serializers import (TeamSerializer, TeamDetailsSerializer, PlayerScoreSerializer,
                                     TeamWeeklyScoreSerializer, WeekSerializer, WindowSerializer,
                                     TeamMonthlyScoreSerializer, AUCTION_LOG_FILE)
from rest_framework.response import Response


class AuthUserView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'username': request.user.username})


class ConstantsView(APIView):
    def get(self, request, *args, **kwargs):
        data = {}
        constants = Constant.objects.all()
        for constant in constants:
            data[constant.name] = constant.value
        return Response(data)


class UserTeamView(APIView):
    def get(self, request, *args, **kwargs):
        # get the team for the user by username url parameter
        username = kwargs['username']
        if username:
            team = Team.active_objects.get(manager__username=username)
            return Response(TeamSerializer(team).data)
        # else
        return Response({'detail': 'Team not found.'}, status=status.HTTP_404_NOT_FOUND)


class AuctionNominationSummaryView(APIView):

    def get(self, request, *args, **kwargs):
        # this view is only used from Admin-only pages, but belt and braces...
        if not request.user.is_superuser:
            return Response({'detail': 'Team not found.'}, status=status.HTTP_401_UNAUTHORIZED)

        data = []
        teams = Team.active_objects.exclude(manager__username__in=['Admin', 'admin'])

        position_dict = dict(Player.POSITION)

        for team in teams:
            nominations = AuctionNomination.objects.select_related('player', 'manager').filter(team=team)
            summary_dict = {'name': team.manager.username}
            # group by player position and count the values
            counts = nominations.values('player__position').annotate(Count('id'))
            for c in counts:
                position = position_dict[c['player__position']]
                summary_dict[position] = c['id__count']
            data.append(summary_dict)

        return Response(data)


class AuctionTeamSummaryView(APIView):
    """
    Provide summary data for each Team during auction.
    """
    def get(self, request, *args, **kwargs):
        # TODO - review this
        # Adding this view for all users.  Only the admin will see the controls to get random players
        # # this view is only used from Admin-only pages, but belt and braces...
        # if not request.user.is_superuser:
        #     return Response({'detail': 'Unauthorized Access.'}, status=status.HTTP_401_UNAUTHORIZED)

        data = {}
        teams = Team.active_objects.exclude(manager__username__in=['Admin', 'admin'])
        funds_per_player = 100.0 / 15

        position_dict = dict(Player.POSITION)

        for team in teams:
            # update the funds available based on players bought so far
            team.update_funds()
            players = Player.objects.select_related('team__manager').filter(team=team)
            data[team.id] = {
                'manager': team.manager.username,
                'funds': team.funds,
                'players': {
                    position_dict[Player.GKP]: [],
                    position_dict[Player.DEF]: [],
                    position_dict[Player.MID]: [],
                    position_dict[Player.STR]: [],
                },
                'bought': 0,
                'funds_per_player': funds_per_player,
            }
            for p in players:
                data[team.id]['players'][p.get_position_display()].append(p.sale)
                data[team.id]['bought'] += 1
                # calculate the average funds per player left to buy
                if data[team.id]['funds'] == 0 or data[team.id]['bought'] >= 15:
                    # avoid zero division errors and allow for squad players
                    data[team.id]['funds_per_player'] = data[team.id]['funds']
                else:
                    data[team.id]['funds_per_player'] = data[team.id]['funds'] / (15 - data[team.id]['bought'])

        return Response(data)


class AuctionRandomPlayerCodesView(APIView):
    """
    Return a list of nominated player codes.
    """
    def get(self, request, *args, **kwargs):
        window = get_current_window()
        filter_kwargs = {"player__team__isnull": True}
        if window.type in [Window.AUCTION_NOMINATION, Window.AUCTION]:
            nomination_model = AuctionNomination
            filter['passed'] = False
        else:
            nomination_model = TransferNomination
        # create a list of player codes nominated for the auction but not assigned to a team
        nominated_player_codes = nomination_model.objects.select_related(
            'player'
        ).filter(
            **filter_kwargs
        ).order_by(
            'player__code'
        ).values_list(
            'player__code',
            flat=True
        ).distinct()

        nominated_player_codes = list(nominated_player_codes)

        # randomise the list
        random.shuffle(nominated_player_codes)

        return Response(nominated_player_codes)


class AuctionPassNominationsView(APIView):
    """
    Pass all nominations for a particular player.
    """
    def get(self, request, *args, **kwargs):
        auction_nominations = AuctionNomination.objects.select_related(
            'player'
        ).filter(
            player__id=kwargs['player_id']
        )

        player = auction_nominations.first().player

        for nomination in auction_nominations:
            nomination.passed = True
            nomination.save()

        if not player.team:
            # log the action
            with open(AUCTION_LOG_FILE, 'a') as outfile:
                msg = "{} {} ({}) {} - was returned to the pool".format(
                    player.code,
                    player.name,
                    player.prem_team,
                    player.value
                )
                outfile.write(msg + "\n")

        return Response({"success": True})


class AuctionDealLogsView(APIView):
    """
    Return all auction deal log messages.
    """
    def get(self, request, *args, **kwargs):
        deals = []
        with open(AUCTION_LOG_FILE, 'r') as infile:
            deals = [line.rstrip('\n') for line in infile]

        deals.reverse()
        return Response({"deals": deals[:20]})


class TeamDetailsView(APIView):

    def get(self, request, **kwargs):
        team = Team.active_objects.filter(
            id=kwargs['id']
        ).first()

        data = TeamDetailsSerializer(team).data
        # identify whether the user is the manager of this team
        data['is_manager'] = True if request.user == team.manager else False

        # # include a list of status choices (except for the first one: 'Available')
        data['status_choices'] = [{'name': s[1], 'value': s[0]} for s in Player.STATUS][1:]

        return Response(data)


class TeamScoresView(APIView):

    def get(self, request, *args, **kwargs):
        team = Team.active_objects.filter(
            id=kwargs['id']
        ).prefetch_related(
            'manager', 'players', 'weekly_scores', 'monthly_scores'
        ).first()

        data = {}

        month = request.GET.get('month', None)
        if month:
            month = int(month)

        weeks, player_scores, weekly_scores = get_weeks_and_scores_for_month(team, month)
        data['weeks'] = WeekSerializer(weeks, many=True).data
        data['player_scores'] = PlayerScoreSerializer(player_scores, many=True).data
        data['weekly_scores'] = TeamWeeklyScoreSerializer(weekly_scores, many=True).data

        if weekly_scores:
            data['player_ids'] = list(player_scores.values_list('player', flat=True).order_by('player').distinct())
        else:
            # if there are no scores yet for the month, then just display the current team
            data['player_ids'] = [player.id for player in team.players.all()]

        # add any currently inactive players to the list
        inactive_players = Player.objects.filter(team=team, is_active=False)
        if inactive_players:
            data['player_ids'] += [player.id for player in inactive_players]
            data['player_ids'].sort()

        return Response(data)


class TeamLineupView(APIView):

    def get(self, request, *args, **kwargs):
        team = Team.active_objects.get(id=kwargs['id'])
        data = TeamDetailsSerializer(team).data
        # identify whether the user is the manager of this team
        data['is_manager'] = True if request.user == team.manager else False

        # TODO - add scores for the month in here

        # include a list of status choices (except for the first one: 'Available')
        data['status_choices'] = [{'name': s[1], 'value': s[0]} for s in Player.STATUS][1:]

        return Response(data)


class TeamValidateView(APIView):

    def get(self, request, *args, **kwargs):
        team = Team.active_objects.get(id=kwargs['id'])
        data = {'is_valid': team.validate_line_up()}

        return Response(data)


# class UpdateScoresView(APIView):
#
#     def get(self, request, *args, **kwargs):
#         # this view is only used with Admin-only functions, but just to be sure...
#         if not request.user.is_superuser:
#             return Response({'detail': 'Unauthorized Access.'}, status=status.HTTP_401_UNAUTHORIZED)
#
#         try:
#             week = get_week()
#             # check the update is being requested on the correct day
#             if date.today() != week.date:
#                 print("UpdateScoresView: update requested too early - ", date.today())
#                 detail = ('Update requested too early.  Please try again on {}, or use the recalculate '
#                           'scores function specifying a week.'.format(week.date))
#                 print(detail)
#                 return Response({'detail': detail}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#             print("UpdateScoresView: getting player update for week ", week)
#             update_players(week)
#             print("UpdateScoresView: updating team scores for week ", week)
#             update_weekly_scores(week)
#             print("UpdateScoresView: update completed successfully!")
#             return Response({'detail': 'Update successfully completed.'}, status=status.HTTP_200_OK)
#         except Exception, err:
#             print("Exceptions:", Exception)
#             print("err:", err)
#             import traceback
#             traceback.print_exc()
#             print("UpdateScoresView: error occurred during update!")
#             return Response({'detail': 'Error with update.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CurrentWindowView(APIView):

    def get(self):
        window = get_current_window()
        data = WindowSerializer(window).data
        return Response(data)


class ProcessTransfersForTeamView(APIView):
    def get(self, request, *args, **kwargs):
        team = Team.active_objects.get(id=kwargs['id'])
        messages = process_transfer_outcomes(team)
        data = {'messages': messages}
        return Response(data)


class ManagerOfTheMonthView(APIView):
    """
    Return TeamMonthlyScores for the current month and previous months.
    """
    def get(self, request):
        months = get_months_to_date()
        data = []
        for month in months:
            scores = TeamMonthlyScore.objects.filter(month=month).order_by('-value')
            if scores:
                data.append({
                    'month': month_name[month],
                    'scores': TeamMonthlyScoreSerializer(scores, many=True).data
                })
        return Response(data)
