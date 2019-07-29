import random
# import os
# from dateutil.relativedelta import relativedelta
# from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
# from django.db.models import Q

from calendar import month_name
from datetime import date, timedelta

from django.db.models import Count
from django.utils import timezone
from rest_framework import status
# from rest_framework import generics, filters
# from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from ffooty.functions import (get_weeks_and_scores_for_month, get_week, update_players,
                              update_weekly_scores, process_transfer_outcomes,
                              get_months_to_date, )
from ffooty.models import (Constant, Team, AuctionNomination, Player, Window, TeamMonthlyScore,
                           PlayerTeamScore, )
from ffooty.rest.serializers import (TeamSerializer, TeamDetailsSerializer, PlayerScoreSerializer,
                                     TeamWeeklyScoreSerializer, WeekSerializer, WindowSerializer,
                                     TeamMonthlyScoreSerializer, )
# from ffooty.rest.serializers import UserSerializer
from rest_framework.response import Response
# import dateutil.parser
# from ffooty.signals import add_activity_callback


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

        for team in teams:
            nominations = AuctionNomination.objects.select_related('player', 'manager').filter(team=team)
            summary_dict = {'name': team.manager.username}
            # group by player position and count the values
            counts = nominations.values('player__position').annotate(Count('id'))
            for c in counts:
                position = c['player__position']
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

        for team in teams:
            # update the funds available based on players bought so far
            team.update_funds()
            players = Player.objects.select_related('team__manager').filter(team=team)
            data[team.id] = {
                'manager': team.manager.username,
                'funds': team.funds,
                'players': {
                    'G': [],
                    'D': [],
                    'M': [],
                    'S': [],
                },
                'bought': 0,
                'funds_per_player': funds_per_player,
            }
            for p in players:
                data[team.id]['players'][p.position].append(p.sale)
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
        # create a list of player codes nomincated for the auction but not assigned to a team
        nominated_player_codes = AuctionNomination.objects.select_related(
            'player'
        ).filter(
            player__team__isnull=True,
            passed=False
        ).order_by(
            'player__code'
        ).values_list(
            'player__code',
            flat=True
        ).distinct()

        nominated_player_codes = list(nominated_player_codes)

        # randomise the list
        random.shuffle(nominated_player_codes)
        print "****"
        print "nominated_player_codes[:10] =", nominated_player_codes[:10]
        print "****"

        return Response(nominated_player_codes)


class AuctionPassNominationsView(APIView):
    """
    Pass all nominations for a particular player.
    """
    def get(self, request, *args, **kwargs):
        auction_nominations = AuctionNomination.objects.filter(
            player__id=kwargs['player_id']
        )

        for nomination in auction_nominations:
            nomination.passed = True
            nomination.save()

        return Response({"success": True})


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
        ).select_related(
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


class UpdateScoresView(APIView):

    def get(self, request, *args, **kwargs):
        # this view is only used with Admin-only functions, but just to be sure...
        if not request.user.is_superuser:
            return Response({'detail': 'Unauthorized Access.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            week = get_week()
            # check the update is being requested on the correct day
            if date.today() != week.date:
                print "UpdateScoresView: update requested too early - ", date.today()
                detail = ('Update requested too early.  Please try again on {}, or use the recalculate '
                          'scores function specifying a week.'.format(week.date))
                print detail
                return Response({'detail': detail}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            print "UpdateScoresView: getting player update for week ", week
            update_players(week)
            print "UpdateScoresView: updating team scores for week ", week
            update_weekly_scores(week)
            print "UpdateScoresView: update completed successfully!"
            return Response({'detail': 'Update successfully completed.'}, status=status.HTTP_200_OK)
        except Exception, err:
            print "Exceptions:", Exception
            print "err:", err
            import traceback
            traceback.print_exc()
            print "UpdateScoresView: error occurred during update!"
            return Response({'detail': 'Error with update.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CurrentWindowView(APIView):

    def get(self):
        now = timezone.now()
        window = Window.objects.filter(open_from__lte=now, deadline__gte=now).first()
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

#
#
# class ActivityStreamList(generics.ListCreateAPIView):
#     queryset = ActivityStream.objects.all()
#     serializer_class = ActivityStreamSerializer
#     paginate_by = 2
#
#     def get_queryset(self):
#         queryset = self.queryset
#         space = int(self.request.QUERY_PARAMS.get('space', 0))
#         if space != 0:  # 0 means focus is on user's personal space
#             queryset = queryset.filter(space__pk=space)
#         else:
#             # Only get spaces the user is a member of
#             queryset = queryset.filter(Q(space__groups__in=self.request.user.group_set.all()) | Q(user=self.request.user))
#         since = self.request.QUERY_PARAMS.get('since', None)
#         if since is not None:
#             d1 = dateutil.parser.parse(since)
#             queryset = queryset.filter(added__gte=d1)
#         return queryset
#
#     def create(self, request, *args, **kwargs):
#         ''' Override the create method to use the ActivityWriteSerializer '''
#         data = request.DATA
#         data['user'] = self.request.user.id
#         serializer = ActivityStreamWriteSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class ActivityComment(generics.ListCreateAPIView):
#     serializer_class = CommentReadSerializer
#     queryset = Comment.objects.all()
#
#     def get_queryset(self):
#         queryset = self.queryset
#         space = int(self.request.QUERY_PARAMS.get('space', 0))
#         if space != 0:
#             queryset = queryset.filter(activity__space__pk=space)
#         else:
#             # Only get spaces the user is a member of
#             queryset = queryset.filter(activity__space__groups__in=self.request.user.group_set.all())
#         activity = self.request.QUERY_PARAMS.get('activity', None)
#         if activity is not None:
#             queryset = queryset.filter(activity__pk=activity)
#         since = self.request.QUERY_PARAMS.get('since', None)
#         if since is not None:
#             d1 = dateutil.parser.parse(since) + relativedelta(microseconds=1000) # Add 1ms because JS does not have microsecond resolution
#             queryset = queryset.filter(added__gt=d1)
#         return queryset
#
#     def create(self, request, *args, **kwargs):
#         data = request.DATA
#         data['user'] = self.request.user.id
#         serializer = CommentWriteSerializer(data=data, files=request.FILES)
#         if serializer.is_valid():
#             self.pre_save(serializer.object)
#             self.object = serializer.save(force_insert=True)
#             self.post_save(self.object, created=True)
#             headers = self.get_success_headers(serializer.data)
#             serializer = CommentReadSerializer(serializer.object)
#             return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class StatusUpdate(generics.CreateAPIView):
#     serializer_class = StatusUpdateSerializer
#
#     def create(self, request, *args, **kwargs):
#         data = request.DATA
#         data['user'] = self.request.user.id
#         serializer = self.serializer_class(data=data)
#         if serializer.is_valid():
#             headers = self.get_success_headers(serializer.data)
#             space = Space.objects.get(id=data['space'])
#             activity = add_activity_callback(sender=self.__class__, user=self.request.user, space=space, content_object=self.request.user, message=data['message'])
#             serializer = ActivityStreamSerializer(activity)
#             return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

