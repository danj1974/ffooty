from django.conf.urls import patterns, include, url

from rest_framework.routers import DefaultRouter

from rest.views import (
    AuthUserView, ConstantsView, UserTeamView, AuctionNominationSummaryView,
    AuctionTeamSummaryView, TeamDetailsView, TeamLineupView, TeamValidateView,
    UpdateScoresView, ProcessTransfersForTeamView, ManagerOfTheMonthView,
    TeamScoresView, AuctionRandomPlayerCodesView, AuctionPassNominationsView
)
from rest.viewsets import (
    TeamViewSet, PremTeamViewSet, PlayerViewSet, WeekViewSet, PlayerScoreViewSet,
    TeamWeeklyScoreViewSet, TeamTotalScoreViewSet, WindowViewSet,
    AuctionNominationViewSet, ManagerViewSet, TransferNominationViewSet,
    BanterViewSet, CommentViewSet, SquadChangeViewSet
)


urlpatterns = patterns('',
    url(r'^auth_user/$', AuthUserView.as_view(), name='api-auth_user'),
    url(r'^constants/$', ConstantsView.as_view(), name='api-constants'),
    url(r'^userteam/(?P<username>\d+)/$', UserTeamView.as_view(), name='api-userteam'),
    url(r'^auction_nomination_summary/$', AuctionNominationSummaryView.as_view(), name='api-auction_nomination_summary'),
    url(r'^auction_team_summary/$', AuctionTeamSummaryView.as_view(), name='api-auction_team_summary'),
    url(r'^auction_random_player_codes/$', AuctionRandomPlayerCodesView.as_view(), name='api-auction_player_codes'),
    url(r'^auction_pass_nominations/(?P<player_id>[0-9]+)/$', AuctionPassNominationsView.as_view(), name='api-auction_pass_nominations'),
    url(r'^team_details/(?P<id>[0-9]+)/$', TeamDetailsView.as_view(), name='api-team_details'),
    url(r'^team_scores/(?P<id>[0-9]+)/$', TeamScoresView.as_view(), name='api-team_scores'),
    url(r'^team_lineup/(?P<id>[0-9]+)/$', TeamLineupView.as_view(), name='api-team_lineup'),
    url(r'^team_validate/(?P<id>[0-9]+)/$', TeamValidateView.as_view(), name='api-team_validate'),
    url(r'^update_scores/$', UpdateScoresView.as_view(), name='api-update_scores'),
    url(r'^process_transfers_for_team/(?P<id>[0-9]+)/$', ProcessTransfersForTeamView.as_view(), name='api-process_transfers_for_team'),
    url(r'^monthly_scores/$', ManagerOfTheMonthView.as_view(), name='api-monthly_scores'),
)

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