var footyAPI = angular.module('footyAPI', ['ngResource', 'ngCookies']);

// Config
footyAPI.config(['$resourceProvider', '$locationProvider', '$httpProvider', function ($resourceProvider, $locationProvider, $httpProvider) {
    // Don't strip trailing slashes from calculated URLs
    $resourceProvider.defaults.stripTrailingSlashes = false;
    // Enable HTML5 - needs HTML5 doc
    //$locationProvider.html5Mode(true);
    // Ensure CSRF token is sent in $http requests
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.withCredentials = true;
}]);

footyAPI.factory('AuthUser', ['$resource', function($resource) {
    return $resource('/api/auth_user/', {}, {
        get: {method: 'GET', params:{}, isArray: false},
    });
}]);

footyAPI.factory('Managers', ['$resource', function($resource) {
    return $resource('/api/manager/:id/', {}, {
        query: {method: 'GET', params:{}, isArray: true},
        get: {method: 'GET', params:{id: '@id'}, isArray: false},
    });
}]);

footyAPI.factory('UserTeam', ['$resource', function($resource) {
    return $resource('/api/userteam/:username/', {}, {
        get: {method: 'GET', params:{username: '@username'}, isArray: false},
    });
}]);

footyAPI.factory('Teams', ['$resource', function($resource) {
    return $resource('/api/team/:id/', {}, {
        query: {method: 'GET', params:{}, isArray: true},
        get: {method: 'GET', params:{id: '@id'}, isArray: false},
        patch: {method: 'PATCH', params:{id: '@id'}, isArray: false},
    });
}]);

footyAPI.factory('PremTeams', ['$resource', function($resource) {
    return $resource('/api/premteam/:id/', {}, {
        query: {method: 'GET', params:{}, isArray: true},
        get: {method: 'GET', params:{id: '@id'}, isArray: false},
    });
}]);


footyAPI.factory('Players', ['$resource', function($resource) {
    return $resource('/api/player/:id/', {}, {
        query: {method: 'GET', params:{}, isArray: true},
        get: {method: 'GET', params:{id: '@id'}, isArray: false},
        patch: {method: 'PATCH', params:{id: '@id'}, isArray: false},
    });
}]);

footyAPI.factory('ReturnPlayerToPool', ['$resource', function($resource) {
    return $resource('/api/player/:id/return_to_pool/', {}, {
        patch: {method: 'PATCH', params:{id: '@id'}, isArray: false},
    });
}]);

footyAPI.factory('Weeks', ['$resource', function($resource) {
    return $resource('/api/week/:id/', {}, {
        query: {method: 'GET', params:{}, isArray: true},
        get: {method: 'GET', params:{id: '@id'}, isArray: false},
    });
}]);

footyAPI.factory('PlayerScores', ['$resource', function($resource) {
    return $resource('/api/playerscore/:id/', {}, {
        query: {method: 'GET', params:{}, isArray: true},
        get: {method: 'GET', params:{id: '@id'}, isArray: false},
    });
}]);

footyAPI.factory('TeamWeeklyScores', ['$resource', function($resource) {
    return $resource('/api/teamweeklyscore/:id/', {}, {
        query: {method: 'GET', params:{}, isArray: true},
        get: {method: 'GET', params:{id: '@id'}, isArray: false},
    });
}]);

footyAPI.factory('TeamTotalScores', ['$resource', function($resource) {
    return $resource('/api/teamtotalscore/:id/', {}, {
        query: {method: 'GET', params:{}, isArray: true},
        get: {method: 'GET', params:{id: '@id'}, isArray: false},
    });
}]);

footyAPI.factory('Windows', ['$resource', function($resource) {
    return $resource('/api/window/:id/', {}, {
        query: {method: 'GET', params:{}, isArray: true},
        get: {method: 'GET', params:{id: '@id'}, isArray: false},
    });
}]);

footyAPI.factory('CurrentWindow', ['$resource', function($resource) {
    return $resource('/api/window/get_current/', {}, {
        query: {method: 'GET', params:{}, isArray: false},
//        get: {method: 'GET', params:{id: '@id'}, isArray: false},
    });
}]);

footyAPI.factory('AuctionNominations', ['$resource', function($resource) {
    return $resource('/api/auctionnomination/:id/', {}, {
        query: {method: 'GET', params:{}, isArray: true},
        get: {method: 'GET', params:{id: '@id'}, isArray: false},
        put: {method: 'PUT', params:{id: '@id'}, isArray: false},
        patch: {method: 'PATCH', params:{id: '@id'}, isArray: false},
        remove: {method: 'DELETE', params:{id: '@id'}, isArray: false}
    });
}]);

footyAPI.factory('TransferNominations', ['$resource', function($resource) {
    return $resource('/api/transfernomination/:id/', {}, {
        query: {method: 'GET', params:{}, isArray: true},
        get: {method: 'GET', params:{id: '@id'}, isArray: false},
        put: {method: 'PUT', params:{id: '@id'}, isArray: false},
        patch: {method: 'PATCH', params:{id: '@id'}, isArray: false},
        remove: {method: 'DELETE', params:{id: '@id'}, isArray: false}
    });
}]);

footyAPI.factory('TransferNominationPlayerDetails', ['$resource', function($resource) {
    return $resource('/api/transfernomination/with_player_details/', {}, {
        query: {method: 'GET', params:{}, isArray: false},
    });
}]);

footyAPI.factory('TransferNominationSummary', ['$resource', function($resource) {
    return $resource('/api/transfernomination/summary/', {}, {
        query: {method: 'GET', params:{}, isArray: false},
    });
}]);

footyAPI.factory('AcceptBid', ['$resource', function($resource) {
    return $resource('/api/transfernomination/:id/accept_bid/', {}, {
        patch: {method: 'PATCH', params:{id: '@id'}, isArray: false},
    });
}]);

footyAPI.factory('PassOnBid', ['$resource', function($resource) {
    return $resource('/api/transfernomination/:id/pass_on_bid/', {}, {
        patch: {method: 'PATCH', params:{id: '@id'}, isArray: false},
    });
}]);

footyAPI.factory('ProcessTransfersForTeam', ['$resource', function($resource) {
    return $resource('/api/process_transfers_for_team/:id', {}, {
        get: {method: 'GET', params:{id: '@id'}, isArray: false},
    });
}]);

footyAPI.factory('SquadChanges', ['$resource', function($resource) {
    return $resource('/api/squadchange/:id/', {}, {
        query: {method: 'GET', params:{}, isArray: true},
        get: {method: 'GET', params:{id: '@id'}, isArray: false},
        put: {method: 'PUT', params:{id: '@id'}, isArray: false},
        patch: {method: 'PATCH', params:{id: '@id'}, isArray: false},
        remove: {method: 'DELETE', params:{id: '@id'}, isArray: false}
    });
}]);

footyAPI.factory('Banter', ['$resource', function($resource) {
    return $resource('/api/banter/:id/', {}, {
        query: {method: 'GET', params:{}, isArray: true},
        get: {method: 'GET', params:{id: '@id'}, isArray: false},
        put: {method: 'PUT', params:{id: '@id'}, isArray: false},
        patch: {method: 'PATCH', params:{id: '@id'}, isArray: false},
        remove: {method: 'DELETE', params:{id: '@id'}, isArray: false}
    });
}]);

footyAPI.factory('Comment', ['$resource', function($resource) {
    return $resource('/api/comment/:id/', {}, {
        query: {method: 'GET', params:{}, isArray: true},
        get: {method: 'GET', params:{id: '@id'}, isArray: false},
        put: {method: 'PUT', params:{id: '@id'}, isArray: false},
        patch: {method: 'PATCH', params:{id: '@id'}, isArray: false},
        remove: {method: 'DELETE', params:{id: '@id'}, isArray: false}
    });
}]);

footyAPI.factory('Constants', ['$resource', function($resource) {
    return $resource('/api/constants/', {}, {
        get: {method: 'GET', params:{}, isArray: false},
    });
}]);

footyAPI.factory('AuctionNominationSummary', ['$resource', function($resource) {
    return $resource('/api/auction_nomination_summary/', {}, {
        query: {method: 'GET', params:{}, isArray: true},
    });
}]);

footyAPI.factory('AuctionTeamSummary', ['$resource', function($resource) {
    return $resource('/api/auction_team_summary/', {}, {
        query: {method: 'GET', params:{}, isArray: false},
    });
}]);

footyAPI.factory('AuctionRandomPlayerCodes', ['$resource', function($resource) {
    return $resource('/api/auction_random_player_codes/', {}, {
        query: {method: 'GET', params:{}, isArray: true},
    });
}]);

footyAPI.factory('TeamDetails', ['$resource', function($resource) {
    return $resource('/api/team_details/:id/', {}, {
        get: {method: 'GET', params:{id: '@id'}, isArray: false},
    });
}]);

footyAPI.factory('TeamScores', ['$resource', function($resource) {
    return $resource('/api/team_scores/:id/', {}, {
        get: {method: 'GET', params:{id: '@id'}, isArray: false},
    });
}]);

footyAPI.factory('TeamValidate', ['$resource', function($resource) {
    return $resource('/api/team_validate/:id/', {}, {
        get: {method: 'GET', params:{id: '@id'}, isArray: false},
    });
}]);
//
//footyAPI.factory('SquadChanges', ['$resource', function($resource) {
//    return $resource('/api/squadchange/:id/', {}, {
//        get: {method: 'GET', params:{id: '@id'}, isArray: false},
//    });
//}]);

footyAPI.factory('UpdateScores', ['$resource', function($resource) {
    return $resource('/api/update_scores/', {}, {
        get: {method: 'GET', params:{}, isArray: false},
    });
}]);

footyAPI.factory('MonthlyScores', ['$resource', function($resource) {
    return $resource('/api/monthly_scores/', {}, {
        get: {method: 'GET', params:{}, isArray: true},
    });
}]);

//footyAPI.factory('FileStorage', ['$resource', function($resource) {
//    return $resource('/api/files/:id/', {}, {
//        get: {method: 'GET', params:{id: '@id'}, isArray: false},
//        query: {method: 'GET', params:{}, isArray: true},
//        post: {method: 'POST',
//            transformRequest: angular.identity,
//            headers: {'Content-Type': undefined}, // Leave browser to set to correct type and boundary
//            isArray: false,
//            params:{id: '@id'},
//        },
//        rename: {method: 'PATCH', params:{id: '@id'}, isArray: false},
//        remove: {method: 'DELETE', params:{id: '@id'}, isArray: false},
//    });
//}]);
//
//footyAPI.factory('FileStoragePaths', ['$resource', function($resource) {
//    return $resource('/api/filepaths/:id/', {}, {
//        get: {method: 'GET', params:{id: '@id'}, isArray: false},
//        query: {method: 'GET', params:{}, isArray: true},
//        post: {method: 'POST', params:{}, isArray: false},
//        put: {method: 'PUT', params:{}, isArray: false},
//        rename: {method: 'PATCH', params:{id: '@id'}, isArray: false},
//        remove: {method: 'DELETE', params:{id: '@id'}, isArray: false},
//    });
//}]);
//
//
//footyAPI.factory('ActivityStream', ['$resource', function($resource) {
//    return $resource('/api/activity/', {}, {
//        query: {method: 'GET', params:{}, isArray: false},
//        post: {method: 'POST', params:{}, isArray: false},
//    });
//}]);
//
//footyAPI.factory('ActivityComment', ['$resource', function($resource) {
//    return $resource('/api/comment/', {}, {
//        query: {method: 'GET', params:{}, isArray: true},
//        post: {method: 'POST', params:{}, isArray: false},
//    });
//}]);
//
//footyAPI.factory('StatusUpdate', ['$resource', function($resource) {
//    return $resource('/api/statusupdate/', {}, {
//        post: {method: 'POST', params:{}, isArray: false},
//    });
//}]);
//
//
//footyAPI.service('ActivityService', ['$route', 'ActivityStream', function($route, ActivityStream) {
//
//	this.post = function(message) {
//		return ActivityStream.save({message: message,
//									space: $route.current.params.space_id,
//								    plugin: $route.current.params.app_id});
//	};
//}]);

