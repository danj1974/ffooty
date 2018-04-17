footyApp.config(['$routeProvider', '$locationProvider', 'TEMPLATE_PATH', function($routeProvider, $locationProvider, TEMPLATE_PATH) {
    $locationProvider.html5Mode(false);
    $routeProvider.when('/', {
        redirectTo: '/home/'
    }).when('/home/', {
        controller: 'BaseController',
        templateUrl: TEMPLATE_PATH + 'main-panel/home.html',
        resolve: {
    		teamRunningTotals: ['TeamRunningTotals', function(TeamRunningTotals) {
	            console.log('resolving TeamRunningTotals...');
	            return TeamRunningTotals.get().$promise;
	        }],
    	}
    }).when('/admin/:admin_key/auction_nominations', {
        controller: 'AdminAuctionNominationsController',
        templateUrl: TEMPLATE_PATH + 'main-panel/admin/auction_nominations.html',
        resolve: {
    		nominationSummary: ['$rootScope', 'AuctionNominationSummary', function($rootScope, AuctionNominationSummary) {
                console.log('admin: resolving nominationSummary...');
                return AuctionNominationSummary.query().$promise;
            }],
    	}
    }).when('/admin/:admin_key/auction', {
        controller: 'AdminAuctionTeamsController',
        templateUrl: TEMPLATE_PATH + 'main-panel/admin/auction.html',
        resolve: {
    		auctionTeamSummary: ['$rootScope', 'AuctionTeamSummary', function($rootScope, AuctionTeamSummary) {
                console.log('admin: resolving auctionTeamSummary...');
                return AuctionTeamSummary.query().$promise;
            }],
            auctionRandomPlayerCodes: ['$rootScope', 'AuctionRandomPlayerCodes', function($rootScope, AuctionRandomPlayerCodes) {
                console.log('admin: resolving auctionRandomPlayerCodes...');
                return AuctionRandomPlayerCodes.query().$promise;
            }],
            teams: ['$rootScope', 'Teams', function($rootScope, Teams) {
                console.log('admin: resolving Teams...');
                return Teams.query().$promise;
            }],
    	}
    }).when('/auction/', {
        controller: 'AdminAuctionTeamsController',
        templateUrl: TEMPLATE_PATH + 'main-panel/admin/auction.html',
        resolve: {
    		auctionTeamSummary: ['$rootScope', 'AuctionTeamSummary', function($rootScope, AuctionTeamSummary) {
                console.log('admin: resolving auctionTeamSummary...');
                return AuctionTeamSummary.query().$promise;
            }],
            auctionRandomPlayerCodes: ['$rootScope', 'AuctionRandomPlayerCodes', function($rootScope, AuctionRandomPlayerCodes) {
                console.log('admin: resolving auctionRandomPlayerCodes...');
                return AuctionRandomPlayerCodes.query().$promise;
            }],
            teams: ['$rootScope', 'Teams', function($rootScope, Teams) {
                console.log('admin: resolving Teams...');
                return Teams.query().$promise;
            }],
    	}
    }).when('/players/', {
        controller: 'PlayersBaseController',
        templateUrl: TEMPLATE_PATH + 'main-panel/loading.html',
        resolve: {
    		players: ['Players', function(Players) {
	            console.log('resolving players...');
	            return Players.query().$promise
	        }],
	        currentWindow: ['CurrentWindow', function(CurrentWindow) {
	            console.log('resolving currentWindow...');
	            return CurrentWindow.query().$promise
	        }],
    	}
     }).when('/players/list/', {
        controller: 'PlayersListController',
        templateUrl: TEMPLATE_PATH + 'main-panel/players/players_list.html',
        resolve: {
//    		players: ['Players', function(Players) {
//	            console.log('resolving players...');
//	            return Players.query().$promise
//	        }],
//	        currentWindow: ['CurrentWindow', function(CurrentWindow) {
//	            console.log('resolving currentWindow...');
//	            return CurrentWindow.query().$promise
//	        }],
    	}
    }).when('/players/auction/list/', {
        controller: 'AuctionListController',
//        templateUrl: TEMPLATE_PATH + 'main-panel/players/players.html',
        template: '<div ng-include="getTemplateUrl()"></div>',
        resolve: {
            userNoms: ['$rootScope', 'AuctionNominations', function($rootScope, AuctionNominations) {
                console.log('resolving auctionNominations...');
                return AuctionNominations.query().$promise;
            }],
            currentWindow: ['CurrentWindow', function(CurrentWindow) {
	            console.log('resolving currentWindow...');
	            return CurrentWindow.query().$promise
	        }],
        }
    }).when('/players/auction/summary/', {
        controller: 'AuctionSummaryController',
//        templateUrl: TEMPLATE_PATH + 'main-panel/players/players.html',
        template: '<div ng-include="getTemplateUrl()"></div>',
        resolve: {
            userNoms: ['$rootScope', 'AuctionNominations', function($rootScope, AuctionNominations) {
                console.log('resolving auctionNominations...');
                return AuctionNominations.query().$promise;
            }],
//            currentWindow: ['CurrentWindow', function(CurrentWindow) {
//	            console.log('resolving currentWindow...');
//	            return CurrentWindow.query().$promise
//	        }],
        }
    }).when('/players/auction/nominations/', {
        controller: 'AuctionNominationsController',
        templateUrl: TEMPLATE_PATH + 'main-panel/players/player_auction_nomination_summary.html',
        resolve: {
            userNoms: ['$rootScope', 'AuctionNominations', function($rootScope, AuctionNominations) {
                console.log('resolving auctionNominations...');
                return AuctionNominations.query().$promise;
            }],
        }
    }).when('/players/auction/selection/', {
        controller: 'AuctionSelectionController',
        templateUrl: TEMPLATE_PATH + 'main-panel/players/player_auction_selection.html',
        resolve: {
            userNoms: ['$rootScope', 'AuctionNominations', function($rootScope, AuctionNominations) {
                console.log('resolving auctionNominations...');
                return AuctionNominations.query().$promise;
            }],
            currentWindow: ['CurrentWindow', function(CurrentWindow) {
	            console.log('resolving currentWindow...');
	            return CurrentWindow.query().$promise
	        }],
        }
    }).when('/players/transfer/list/', {
        controller: 'TransferListController',
        templateUrl: TEMPLATE_PATH + 'main-panel/players/players_transfer_list.html',
        resolve: {
            userTransferNoms: ['$rootScope', 'TransferNominations', function($rootScope, TransferNominations) {
                console.log('resolving transferNominations...');
                return TransferNominations.query().$promise;
            }],
        }
//    }).when('/players/nominations/', {
//        controller: 'PlayerNominationsController',
//        templateUrl: TEMPLATE_PATH + 'main-panel/players/player_nomination_summary.html',
//        resolve: {
//            userNoms: ['$rootScope', 'AuctionNominations', function($rootScope, AuctionNominations) {
//                console.log('resolving auctionNominations...');
//                return AuctionNominations.query().$promise;
//            }],
//        }
    }).when('/transfers/' , {
        controller: 'TransferRedirectController',
        templateUrl: TEMPLATE_PATH + 'main-panel/transfers/transfers_confirmation.html',
        resolve: {
            players: ['Players', function(Players) {
	            console.log('resolving players...');
	            return Players.query().$promise
	        }],
            currentWindow: ['CurrentWindow', function(CurrentWindow) {
                console.log('resolving currentWindow...');
                return CurrentWindow.query().$promise;
            }],
        }
    }).when('/transfers/players_list/' , {
        controller: 'TransferListController',
        templateUrl: TEMPLATE_PATH + 'main-panel/transfers/players_transfer_list.html',
        resolve: {
            userTransferNoms: ['$rootScope', 'TransferNominations', function($rootScope, TransferNominations) {
                console.log('resolving transferNominations...');
                return TransferNominations.query().$promise;
            }],
        }
    }).when('/transfers/selection/', {
        controller: 'TransferSelectionController',
        templateUrl: TEMPLATE_PATH + 'main-panel/transfers/players_transfer_selection.html',
        resolve: {
            userTransferNoms: ['$rootScope', 'TransferNominations', function($rootScope, TransferNominations) {
                console.log('resolving transferNominations...');
                return TransferNominations.query().$promise;
            }],
        }
    }).when('/transfers/summary/', {
        controller: 'TransferSummaryController',
        templateUrl: TEMPLATE_PATH + 'main-panel/transfers/transfers_summary.html',
        resolve: {
//            transferNominationSummary: ['$rootScope', 'TransferNominationSummary', function($rootScope, TransferNominationPlayerDetails) {
            transferNominationSummary: ['$rootScope', 'TransferNominationSummary', function($rootScope, TransferNominationSummary) {
                console.log('resolving userNominationDetails...');
                return TransferNominationSummary.query().$promise;
            }],
        }
    }).when('/transfers/confirmation/', {
        controller: 'TransferConfirmationController',
        templateUrl: TEMPLATE_PATH + 'main-panel/transfers/transfers_confirmation.html',
//        resolve: {
//            userNominationDetails: ['$rootScope', 'TransferNominationPlayerDetails', function($rootScope, TransferNominationPlayerDetails) {
//                console.log('resolving userNominationDetails...');
//                return TransferNominationPlayerDetails.query().$promise;
//            }],
//            teamDetails: ['$rootScope', 'TeamDetails',  function($rootScope, TeamDetails) {
//	            console.log('resolving teamDetails...');
//	            return TeamDetails.get({id: $rootScope.userTeam.id}).$promise;
//	        }],
//        }
    }).when('/teams/:team_id/', {
        controller: 'TeamScoresController',
        templateUrl: TEMPLATE_PATH + 'main-panel/teams/team_details.html',
        resolve: {
    		teamDetails: ['$route', 'TeamDetails',  function($route, TeamDetails) {
	            console.log('resolving teamDetails...');
	            return TeamDetails.get({id: $route.current.params.team_id}).$promise
	        }],
	        teamScores: ['$route', 'TeamScores',  function($route, TeamScores) {
	            console.log('resolving teamScores...');
	            return TeamScores.get({id: $route.current.params.team_id}).$promise
	        }],
    	}
    }).when('/motm/', {
        controller: 'MotmController',
        templateUrl: TEMPLATE_PATH + 'main-panel/scores/motm.html',
        resolve: {
    		monthlyScores: ['$route', 'MonthlyScores',  function($route, MonthlyScores) {
	            console.log('resolving MonthlyScores...');
	            return MonthlyScores.get().$promise
	        }],
    	}
    }).when('/teams/:team_id/lineup/', {
        controller: 'TeamLineupController',
        templateUrl: TEMPLATE_PATH + 'main-panel/teams/team_lineup_selection.html',
        resolve: {
    		teamDetails: ['$route', 'TeamDetails',  function($route, TeamDetails) {
	            console.log('resolving teamDetails...');
	            return TeamDetails.get({id: $route.current.params.team_id}).$promise
	        }],
	        currentWindow: ['CurrentWindow', function(CurrentWindow) {
                console.log('resolving currentWindow...');
                return CurrentWindow.query().$promise;
            }],
    	}
    }).otherwise({
        redirectTo: '/home/'
    });
}]);