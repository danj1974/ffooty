# import datetime
# from django.contrib.auth.models import User
# from django.contrib.contenttypes.models import ContentType
# from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from rest_framework import serializers

from ffooty.models import (Team, PremTeam, Player, Week, PlayerScore, TeamWeeklyScore,
                           TeamTotalScore, Window, AuctionNomination, TransferNomination,
                           Banter, Comment, Constant, TeamMonthlyScore, PlayerTeamScore)
# from storage.models import DatabaseFile
# from storage.rest.serializers import FileStorageRetrieveSerializer
# from wiki.models import WikiPageRevision


# class ContentTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ContentType


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'last_login',)


class TeamSerializer(serializers.ModelSerializer):
    manager = ManagerSerializer()
    latest_weekly_score = serializers.IntegerField(read_only=True)

    class Meta:
        model = Team


class TeamWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ['id', 'name']


class PremTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremTeam


class PlayerSerializer(serializers.ModelSerializer):
    # manager = serializers.StringRelatedField()
    prem_team = serializers.StringRelatedField()
    position = serializers.CharField(source='get_position_display')
    auction_nomination_managers = serializers.CharField(read_only=True)
    manager = serializers.SerializerMethodField()

    class Meta:
        model = Player

    def get_manager(self, obj):
        return obj.team.manager.username if obj.team else None


class AdminPlayerSerializer(PlayerSerializer):
    admin_auction_nomination_managers = serializers.ListField(
        read_only=True,
        child=serializers.CharField()
    )


class WeekSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = Week

    def get_date(self, obj):
        return "({day:02d}-{month:02d})".format(day=obj.date.day, month=obj.date.month)


class PlayerScoreSerializer(serializers.ModelSerializer):
    display_value = serializers.CharField()

    class Meta:
        model = PlayerScore


class PlayerTeamScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayerTeamScore


class TeamWeeklyScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamWeeklyScore


class TeamMonthlyScoreSerializer(serializers.ModelSerializer):
    """
    Serializer for :class:`ffooty.models.TeamMonthlyScore`.

    Adds a `manager` field for manager.username.
    """
    manager = serializers.SerializerMethodField()

    class Meta:
        model = TeamMonthlyScore

    def get_manager(self, obj):
        return obj.team.manager.username


class TeamTotalScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamTotalScore


class TeamDetailsSerializer(serializers.ModelSerializer):
    manager = ManagerSerializer()
    players = PlayerSerializer(many=True)
    ex_players = PlayerSerializer(many=True)
    player_team_scores = serializers.SerializerMethodField()

    class Meta:
        model = Team

    def get_player_team_scores(self, obj):
        return {pts.player.id: pts.value for pts in obj.player_team_scores.all()}


class WindowSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')

    class Meta:
        model = Window


class AuctionNominationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionNomination


class TransferNominationSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source='get_status_display')
    is_next_highest_bid = serializers.ReadOnlyField()

    class Meta:
        model = TransferNomination


class SquadChangeSerializer(serializers.ModelSerializer)


class TransferNominationPlayerSerializer(TransferNominationSerializer):
    player = PlayerSerializer()


class BanterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banter


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment


class ConstantSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')
    # value = ser

    class Meta:
        model = Constant
        fields = ('id', 'name', 'type', 'value',)