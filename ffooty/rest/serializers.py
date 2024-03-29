import os

from django.conf import settings
from django.contrib.auth.models import User

from rest_framework import serializers

from ffooty.models import (Team, PremTeam, Player, Week, PlayerScore, TeamWeeklyScore,
                           TeamTotalScore, Window, AuctionNomination, TransferNomination,
                           Banter, Comment, Constant, TeamMonthlyScore, PlayerTeamScore,
                           SquadChange)


AUCTION_LOG_FILE = os.path.join(settings.BASE_DIR, '../data/auction_log.txt')


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'last_login',)


class TeamSerializer(serializers.ModelSerializer):
    manager = ManagerSerializer()
    latest_weekly_score = serializers.IntegerField(read_only=True)

    class Meta:
        model = Team
        fields = '__all__'


class TeamWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ['id', 'name']


class PremTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremTeam
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    # manager = serializers.StringRelatedField()
    prem_team = serializers.StringRelatedField()
    position = serializers.CharField(source='get_position_display')
    auction_nomination_managers = serializers.CharField(read_only=True)
    transfer_nomination_managers = serializers.CharField(read_only=True)
    manager = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = '__all__'

    def get_manager(self, obj):
        return obj.team.manager.username if obj.team else None

    def update(self, instance, validated_data):
        # log the change to auction log file
        old_manager = self.get_manager(instance)
        new_team = validated_data.get('team')
        new_manager = new_team.manager.username if new_team else "pool"
        new_sale = validated_data.get('sale')

        action = ""
        if not old_manager:
            if new_manager:
                action = " was bought by {}".format(new_manager)
        else:
            if (old_manager == new_manager and
                    instance.sale != new_sale):
                action = " - sale value adjusted for {},".format(new_manager)
            else:
                action = " was changed from {} to {}".format(
                    old_manager,
                    new_manager
                )

        with open(AUCTION_LOG_FILE, 'a') as outfile:
            msg = "{} {} ({}){} sale = {}".format(
                instance.code,
                instance.name,
                instance.prem_team,
                action,
                new_sale
            )
            print(msg)
            outfile.write(msg + "\n")

        return super(PlayerSerializer, self).update(instance, validated_data)


class AdminPlayerSerializer(PlayerSerializer):
    admin_auction_nomination_managers = serializers.ListField(
        read_only=True,
        child=serializers.CharField()
    )
    admin_transfer_nomination_managers = serializers.ListField(
        read_only=True,
        child=serializers.CharField()
    )


class WeekSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = Week
        fields = '__all__'

    def get_date(self, obj):
        return "({day:02d}-{month:02d})".format(day=obj.date.day, month=obj.date.month)


class PlayerScoreSerializer(serializers.ModelSerializer):
    display_value = serializers.CharField()

    class Meta:
        model = PlayerScore
        fields = '__all__'


class PlayerTeamScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayerTeamScore
        fields = '__all__'


class TeamWeeklyScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamWeeklyScore
        fields = '__all__'


class TeamMonthlyScoreSerializer(serializers.ModelSerializer):
    """
    Serializer for :class:`ffooty.models.TeamMonthlyScore`.

    Adds a `manager` field for manager.username.
    """
    manager = serializers.SerializerMethodField()

    class Meta:
        model = TeamMonthlyScore
        fields = '__all__'

    def get_manager(self, obj):
        return obj.team.manager.username


class TeamTotalScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamTotalScore
        fields = '__all__'


class TeamDetailsSerializer(serializers.ModelSerializer):
    manager = ManagerSerializer()
    players = PlayerSerializer(many=True)
    ex_players = PlayerSerializer(many=True)
    player_team_scores = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = '__all__'

    def get_player_team_scores(self, obj):
        return {pts.player.id: pts.value for pts in obj.player_team_scores.all()}


class WindowSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')

    class Meta:
        model = Window
        fields = '__all__'


class AuctionNominationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionNomination
        fields = '__all__'


class TransferNominationSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source='get_status_display')
    is_next_highest_bid = serializers.ReadOnlyField()

    class Meta:
        model = TransferNomination
        fields = '__all__'


class SquadChangeSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()
    window = WindowSerializer()

    class Meta:
        model = SquadChange
        fields = ('id', 'player', 'window', 'current_status', 'new_status', 'month', 'processed')


class TransferNominationPlayerSerializer(TransferNominationSerializer):
    player = PlayerSerializer()


class BanterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banter
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ConstantSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')
    # value = ser

    class Meta:
        model = Constant
        fields = ('id', 'name', 'type', 'value',)