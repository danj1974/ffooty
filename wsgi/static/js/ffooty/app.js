var footyApp = angular.module('footyApp', ['ngRoute', 'ngSanitize', 'ngAnimate', 'footyAPI', 'ui.bootstrap', 'angularMoment', 'infinite-scroll', 'angularGrid']);
footyApp.constant('TEMPLATE_PATH', '/static/partials/');
footyApp.constant('STATIC_ROOT', '/static/');
footyApp.constant('ADMIN_KEY', 'r7bqph1k');
footyApp.config(['$resourceProvider', '$httpProvider', function($resourceProvider, $httpProvider) {
    $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

footyApp.run(['$rootScope', 'ADMIN_KEY', 'Constants', 'Weeks', function($rootScope, ADMIN_KEY, Constants, Weeks) {

    $rootScope.ADMIN_KEY = ADMIN_KEY;

    Constants.get().$promise.then(function(response) {
        $rootScope.constants = response;
        console.log("Constants: " + JSON.stringify($rootScope.constants));
    });

    Weeks.query().$promise.then(function(response) {
        $rootScope.weeks = response;
    });

    $rootScope.monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    $rootScope.windowTypes = {
        AUCTION_NOMINATION:  'Auction Nomination',
        AUCTION:  'Auction',
        SQUAD_CHANGE: 'Squad Change',
        TRANSFER_NOMINATION: 'Transfer Nomination',
        TRANSFER_CONFIRMATION: 'Transfer Confirmation',
    };

}]);



