from datetime import datetime

from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .serializers import (TeamSerializer, PremTeamSerializer, PlayerSerializer,
                          WeekSerializer, PlayerScoreSerializer, TeamWeeklyScoreSerializer,
                          TeamTotalScoreSerializer, WindowSerializer,
                          AuctionNominationSerializer, ManagerSerializer,
                          TransferNominationSerializer,
                          BanterSerializer, CommentSerializer,
                          ConstantSerializer, TeamWriteSerializer,
                          TeamMonthlyScoreSerializer, AdminPlayerSerializer,
                          TransferNominationPlayerSerializer, SquadChangeSerializer
                          )
from ffooty.models import (Team, PremTeam, Player, Week, PlayerScore, TeamWeeklyScore,
                           TeamTotalScore, Window, AuctionNomination, TransferNomination,
                           Banter, Comment, Constant, IllegalNominationOperationException,
                           TeamMonthlyScore, SquadChange)

from ffooty.functions import process_transfer_outcomes


class ManagerViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all().exclude(username='Admin')
    serializer_class = ManagerSerializer


class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all().order_by('manager__username')
    serializer_class = TeamSerializer

    def patch(self, request, *args, **kwargs):
        """Override the patch method to use the TeamWriteSerializer."""
        data = request.DATA
        serializer = TeamWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PremTeamViewSet(ModelViewSet):
    queryset = PremTeam.objects.all()
    serializer_class = PremTeamSerializer


class PlayerViewSet(ModelViewSet):
    queryset = Player.objects.extra(
        select={'position_order': Player.CASE_SQL},
        order_by=['position_order', '-value', 'code']
    )

    def get_serializer_class(self):
        print "self.request.user", self.request.user
        print "self.request.user.is_superuser", self.request.user.is_superuser
        if self.request.user.is_superuser:
            print "returning AdminPlayerSerializer..."
            return AdminPlayerSerializer
        return PlayerSerializer

    def list(self, request, *args, **kwargs):
        """
        Filter players using query parameters.

        Returns a serialized list of Players based on the query
        parameters provided. Each parameter must be a valid field name
        for the Player class.  Extends the superclass method.
        """
        if request.GET:
            players = Player.objects.filter(**request.GET.dict())
            return Response(self.get_serializer(players, many=True).data)
        return super(PlayerViewSet, self).list(request, *args, **kwargs)

    @detail_route(methods=['patch'])
    def return_to_pool(self, request, pk=None):
        try:
            player = self.get_object()
            loss = player.return_to_pool()
            message = 'Player {} was successfully sold at a loss of {}m.'.format(player.name, loss)
            return Response({'detail': message}, status=status.HTTP_202_ACCEPTED)
        except:
            error = 'Player {} could not be returned to the pool.'.format(player.name)
            return Response({'detail': error}, status=status.HTTP_400_BAD_REQUEST)


class WeekViewSet(ModelViewSet):
    queryset = Week.objects.all()
    serializer_class = WeekSerializer


class PlayerScoreViewSet(ModelViewSet):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer


class TeamWeeklyScoreViewSet(ModelViewSet):
    queryset = TeamWeeklyScore.objects.all()
    serializer_class = TeamWeeklyScoreSerializer


class TeamMonthlyScoreViewSet(ModelViewSet):
    queryset = TeamMonthlyScore.objects.all()
    serializer_class = TeamMonthlyScoreSerializer


class TeamTotalScoreViewSet(ModelViewSet):
    queryset = TeamTotalScore.objects.all()
    serializer_class = TeamTotalScoreSerializer


class WindowViewSet(ModelViewSet):
    queryset = Window.objects.all()
    serializer_class = WindowSerializer

    @list_route(methods=['get'])
    def get_current(self, request, pk=None):
        """
        Get the current Window if one is active.
        """
        now = timezone.now()
        window = Window.objects.filter(open_from__lte=now, deadline__gte=now).first()
        return Response(WindowSerializer(window).data)


class AuctionNominationViewSet(ModelViewSet):
    # queryset = AuctionNomination.objects.all()
    serializer_class = AuctionNominationSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            print "AuctionNominationViewSet: get_queryset(): user.is_superuser"
            return AuctionNomination.objects.all()
        else:
            print "AuctionNominationViewSet: get_queryset(): normal user"
            return AuctionNomination.objects.filter(team__manager=self.request.user)


class TransferNominationViewSet(ModelViewSet):
    queryset = TransferNomination.objects.all()
    serializer_class = TransferNominationSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            print "TransferNominationViewSet: get_queryset(): user.is_superuser"
            # return TransferNomination.objects.all().select_related('player')
            return None
        else:
            print "TransferNominationViewSet: get_queryset(): normal user"
            return TransferNomination.objects.filter(team__manager=self.request.user).select_related('player').order_by('priority')

    @list_route(methods=['get'])
    def with_player_details(self, request):
        qs = self.get_queryset()
        serializer = TransferNominationSerializer(qs, many=True)
        data = {
            'nominations': serializer.data,
            'players': {},
        }
        for nomination in qs:
            player = PlayerSerializer(nomination.player).data
            data['players'][nomination.player.id] = player
        return Response(data, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def summary(self, request):
        # get the most recent transfer window
        window = Window.objects.filter(type=Window.TRANSFER_NOMINATION).first()
        print "window = ", window.id, window

        teams = Team.objects.all()

        for team in teams:
            process_transfer_outcomes(team)

        # get only processed nominations and order by player & descending bids
        # TODO - figure out why 'transfer_window=window' doesn't work in this query
        # TODO - this workaround depends on the previous transfer window noms being deleted
        qs = TransferNomination.objects.filter(
            processed=True
        ).select_related(
            'player'
        ).order_by('player__code', '-bid')

        print "qs.count():", qs.count()

        serializer = TransferNominationSerializer(qs, many=True)
        data = {
            'nominations': serializer.data,
            'players': {},
            'teams': {},
        }
        for nomination in qs:
            player = PlayerSerializer(nomination.player).data
            data['players'][nomination.player.id] = player

        for team in teams:
            team_data = TeamSerializer(team).data
            data['teams'][team.id] = team_data

        import pprint
        pprint.pprint(data, indent=4)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        # TODO - review this? is it needed?
        """Override the patch method to use the TeamWriteSerializer."""
        data = request.DATA
        print "TransferNominationViewSet.patch: data = " + data
        serializer = TransferNominationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        print "TransferNominationViewSet.create: request.data = ", request.data
        return super(TransferNominationViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        print "TransferNominationViewSet.update: request.data = ", request.data
        return super(TransferNominationViewSet, self).update(request, *args, **kwargs)

    @detail_route(methods=['patch'])
    def accept_bid(self, request, pk=None):
        print "accept_bid(): pk = ", pk
        try:
            self.get_object().accept_bid()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except IllegalNominationOperationException as e:
            return Response({'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['patch'])
    def pass_on_bid(self, request, pk=None):
        print "pass_on_bid(): pk = ", pk
        self.get_object().pass_on_bid()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BanterViewSet(ModelViewSet):
    queryset = Banter.objects.all()
    serializer_class = BanterSerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ConstantViewSet(ModelViewSet):
    queryset = Constant.objects.all()
    serializer_class = ConstantSerializer


class SquadChangeViewSet(ModelViewSet):
    queryset = SquadChange.objects.all()
    serializer_class = SquadChangeSerializer
