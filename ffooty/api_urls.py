from django.urls import path, include

from rest_framework.routers import DefaultRouter

from rest.views import (
    AuthUserView, ConstantsView, UserTeamView, AuctionNominationSummaryView,
    AuctionTeamSummaryView, TeamDetailsView, TeamLineupView, TeamValidateView,
    ProcessTransfersForTeamView, ManagerOfTheMonthView,  # UpdateScoresView
    TeamScoresView, AuctionRandomPlayerCodesView, AuctionPassNominationsView,
    AuctionDealLogsView
)
from rest.viewsets import (
    TeamViewSet, PremTeamViewSet, PlayerViewSet, WeekViewSet, PlayerScoreViewSet,
    TeamWeeklyScoreViewSet, TeamTotalScoreViewSet, WindowViewSet,
    AuctionNominationViewSet, ManagerViewSet, TransferNominationViewSet,
    BanterViewSet, CommentViewSet, SquadChangeViewSet
)


urlpatterns = [
    path('auth_user/', AuthUserView.as_view(), name='api-auth_user'),
    path('constants/', ConstantsView.as_view(), name='api-constants'),
    path('userteam/<str:username>/', UserTeamView.as_view(), name='api-userteam'),
    path('auction_nomination_summary/', AuctionNominationSummaryView.as_view(), name='api-auction_nomination_summary'),
    path('auction_team_summary/', AuctionTeamSummaryView.as_view(), name='api-auction_team_summary'),
    path('auction_random_player_codes/', AuctionRandomPlayerCodesView.as_view(), name='api-auction_player_codes'),
    path('auction_pass_nominations/<int:player_id>/', AuctionPassNominationsView.as_view(), name='api-auction_pass_nominations'),
    path('auction_deal_logs/', AuctionDealLogsView.as_view(), name='api-auction_deal_logs'),
    path('team_details/<int:id>/', TeamDetailsView.as_view(), name='api-team_details'),
    path('team_scores/<int:id>/', TeamScoresView.as_view(), name='api-team_scores'),
    path('team_lineup/<int:id>/', TeamLineupView.as_view(), name='api-team_lineup'),
    path('team_validate/<int:id>/', TeamValidateView.as_view(), name='api-team_validate'),
    # path('update_scores/', UpdateScoresView.as_view(), name='api-update_scores'),
    path('process_transfers_for_team/<int:id>/', ProcessTransfersForTeamView.as_view(), name='api-process_transfers_for_team'),
    path('monthly_scores/', ManagerOfTheMonthView.as_view(), name='api-monthly_scores'),
]

router = DefaultRouter()
router.register(r'manager', ManagerViewSet, 'api-manager')
router.register(r'team', TeamViewSet, 'api-team')
router.register(r'premteam', PremTeamViewSet, 'api-premteam')
router.register(r'player', PlayerViewSet, 'player-team')
router.register(r'week', WeekViewSet, 'api-week')
router.register(r'playerscore', PlayerScoreViewSet, 'api-playerscore')
router.register(r'teamweeklyscore', TeamWeeklyScoreViewSet, 'api-teamweeklyscore')
router.register(r'teamtotalscore', TeamTotalScoreViewSet, 'api-teamtotalscore')
router.register(r'window', WindowViewSet, 'api-window')
router.register(r'auctionnomination', AuctionNominationViewSet, 'api-auctionnomination')
router.register(r'transfernomination', TransferNominationViewSet, 'api-transfernomination')
router.register(r'banter', BanterViewSet, 'api-banter')
router.register(r'comment', CommentViewSet, 'api-comment')
router.register(r'squadchange', SquadChangeViewSet, 'api-squadchange')
# router.register(r'constant', ConstantViewSet, 'api-constant')
urlpatterns += router.urls
