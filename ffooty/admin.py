from django.contrib import admin
from ffooty.models import (Team, PremTeam, Player, Week, PlayerScore, TeamWeeklyScore,
                           TeamTotalScore, TeamTotalScoreArchive, Window, TransferNomination,
                           Banter, Comment, Constant)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(PremTeam)
class PremTeamAdmin(admin.ModelAdmin):
    pass


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    pass


@admin.register(PlayerScore)
class PlayerScoreAdmin(admin.ModelAdmin):
    pass


@admin.register(TeamWeeklyScore)
class TeamWeeklyScoreAdmin(admin.ModelAdmin):
    pass


@admin.register(TeamTotalScore)
class TeamTotalScoreAdmin(admin.ModelAdmin):
    pass


@admin.register(TeamTotalScoreArchive)
class TeamTotalScoreArchiveAdmin(admin.ModelAdmin):
    pass


@admin.register(Window)
class WindowAdmin(admin.ModelAdmin):
    pass


@admin.register(TransferNomination)
class TransferNominationAdmin(admin.ModelAdmin):
    pass


@admin.register(Banter)
class BanterAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Constant)
class ConstantAdmin(admin.ModelAdmin):
    pass
