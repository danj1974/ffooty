footyApp.controller('MenuController', ['$scope', '$location', '$route', '$rootScope', function($scope, $location, $route, $rootScope) {

	$scope.isActive = function(item) {
		var team_id = $route.current.params.team_id;
		return $location.path().indexOf('/' + space_id + item.link) == 0;
		// return $route.current.$$route.regexp.test('/' + space_id + item.link);
	};

	$scope.selectMenuItem = function(item) {
		var space_id = $route.current.params.space_id;
		$location.path('/' + space_id + item.link);
	};

	var setupMenu = function() {
		// Repopulate menu with available apps for the current space
		$scope.menuitems = [].concat(menuitems);
//		var spaceId = parseInt($route.current.params.space_id);
//		angular.forEach(apps, function(app) {
//			if (app.spaces.indexOf(spaceId) > -1 && user_detail.hasPermission(spaceId, 'portal', 'pluggableapp', 'R', app.id)) {
//				$scope.menuitems.push({
//						title: app.name,
//						link: '/pluggable_app/' + app.id + '/',
//						icon_class: 'glyphicon-list-alt'
//				});
//			}
//		});
		$scope.space_id = $route.current.params.space_id;
	};

//	var user_detail;
//	userHelperFactory.then(function(user) {
//		user_detail = user;
//		$rootScope.$on('$routeChangeSuccess', function() {
//			setupMenu();
//		});
//		setupMenu();
//	});


}]);

footyApp.controller('BaseController', ['$scope', '$location', '$rootScope', 'UpdateScores', function($scope, $location, $rootScope, UpdateScores) {
    // load the constants
//    $rootScope.constants = constants;
//    $rootScope.authUser = authUser;
    // redirect to home page
//    $location.path($location.path() + 'home/');

    $scope.updateScores = function() {
        window.alert("Sending request to server to update the scores, please do not close or refresh your browser");

        UpdateScores.get().$promise
            .then(function(response) {
                console.log("response: " + JSON.stringify(response));
                window.alert(response.detail);
            }, function(error) {
                console.log("error: " + JSON.stringify(error));
                window.alert(error.data.detail);
            });

    };

}]);

footyApp.controller('AdminAuctionNominationsController', ['$scope','$rootScope', '$location', 'nominationSummary',  function($scope, $rootScope, $location, nominationSummary) {
    $scope.nominationSummaryData = nominationSummary;
}]);

footyApp.controller('PlayersBaseController', ['$scope', '$location', '$rootScope', 'players', 'currentWindow', function($scope, $location, $rootScope, players, currentWindow) {
    // load the data
    $rootScope.players = players;
    console.log("PlayersBaseController: players[0] = " + JSON.stringify(players[0], null, 4));
    $rootScope.baseUrl = $location.path();
    $rootScope.currentWindow = currentWindow;

    console.log("PlayersBaseController: currentWindow = " + JSON.stringify($scope.currentWindow));
    var windowTypes = $rootScope.windowTypes;

    if (currentWindow.type == windowTypes.AUCTION_NOMINATION) {
        console.log("PlayersBaseController: redirecting to /players/auction/players_list/");
        $location.path($location.path() + 'auction/list/');
    } else if (currentWindow.type == windowTypes.AUCTION) {
        console.log("PlayersBaseController: redirecting to /players/auction/summary/");
        $location.path($location.path() + 'auction/summary/');
    } else {
        console.log("PlayersBaseController: redirecting to /players/list/");
        console.log($location.path() + 'list/');
        $location.path($location.path() + 'list/');
    }

}]);

footyApp.controller('PlayersListController', ['$scope', '$location', '$rootScope', 'TEMPLATE_PATH', function($scope, $location, $rootScope, TEMPLATE_PATH) {

    // if the browser is refreshed on the player list url, redirect to baseUrl to reload the player list
    if ($rootScope.players == undefined) {
        $location.path('/players/');
    }

    var columnDefs = [
        {headerName: "Code", field: "code", width: 60},
        {headerName: "Position", field: "position", width: 60},
        {headerName: "Player", field: "name", width: 100, suppressMenu: true},
        {headerName: "Team", field: "prem_team", width: 60},
        {headerName: "Value", field: "value", width: 60, suppressMenu: true},
        {headerName: "Sale", field: "sale", width: 60, suppressMenu: true},
        {headerName: "Manager", field: "manager", width: 100},
        {headerName: "pts", field: "total_score", width: 60, suppressMenu: true},
    ];

    $rootScope.gridOptions = {
        columnDefs: columnDefs,
        enableFilter: true,
        enableSorting: true,
        ready: onGridReady,
        rowData: $rootScope.players,
        rowSelection: 'multiple',
//        rowSelected: rowSelected,
//        selectionChanged: selectionChange,
        suppressRowClickSelection: true,
    };

    function onGridReady() {
        // resize the columns to fit the container
        $rootScope.gridOptions.api.sizeColumnsToFit();
    };

    // set the options for the position filter button group and a default value
    $scope.filter = {
        options: ['All', 'GKP', 'DEF', 'MID', 'STR'],
        radioModel: 'All',
    }

    $scope.filterOnPosition = function(position) {
        var filterApi = $rootScope.gridOptions.api.getFilterApi('position');
        if (position == 'All') {
            filterApi.selectEverything();
        } else {
            filterApi.selectNothing();
            filterApi.selectValue(position);
        }
        $rootScope.gridOptions.api.onFilterChanged();
    };

}]);

footyApp.controller('AuctionListController', ['$scope', '$location', '$rootScope', 'AuctionNominations', 'userNoms', 'currentWindow', 'TEMPLATE_PATH', function($scope, $location, $rootScope, AuctionNominations, userNoms, currentWindow, TEMPLATE_PATH) {

    // dynamically assign templateUrls according to AuthUser
    $scope.getTemplateUrl = function() {
        if ($rootScope.authUser == 'Admin' || $rootScope.authUser == 'admin') {
            return TEMPLATE_PATH + 'main-panel/players/admin_players_auction.html';
        } else {
//            return TEMPLATE_PATH + 'main-panel/players/players.html';
            return TEMPLATE_PATH + 'main-panel/players/players_auction.html';
        }
    };

    var windowTypes = $rootScope.windowTypes;

    // if the browser is refreshed on the player list url, redirect to baseUrl to reload the player list
    if ($rootScope.players == undefined) {
        $location.path('/players/');
    }

    var columnDefs = [
        {headerName: "Code", field: "code", width: 50},
        {headerName: "Position", field: "position", width: 60},
        {headerName: "Player", field: "name", width: 100, suppressMenu: true},
        {headerName: "Team", field: "prem_team", width: 50},
        {headerName: "Value", field: "value", width: 50, suppressMenu: true},
        {headerName: "pts", field: "last_years_total", width: 50, suppressMenu: true},

    ];

    console.log("AuctionListController: currentWindow = " + JSON.stringify(currentWindow));

    // add a checkbox for selection if during an auction nomination window
    if (currentWindow.type == windowTypes.AUCTION_NOMINATION) {
        console.log("windowTypes = " + JSON.stringify(windowTypes));
        console.log("true currentWindow = " + currentWindow);
        columnDefs.push({headerName: "Select", field: null, width: 50, checkboxSelection: true});  //, comparator: selectionComparator
//    } else if (currentWindow == windowTypes.AUCTION) {
    // add Nomin
    } else if (currentWindow.type == windowTypes.AUCTION) {
        console.log("windowTypes = " + JSON.stringify(windowTypes));
        console.log("false currentWindow = " + JSON.stringify(currentWindow));
        columnDefs.push({headerName: "Manager", field: "manager", width: 50});
        columnDefs.push({headerName: "Nominating Managers", field: "auction_nomination_managers", width: 220});
    } else {
        console.log("else...");
        columnDefs.push({headerName: "Manager", field: "manager", width: 50});
    }

    $rootScope.gridOptions = {
        columnDefs: columnDefs,
        enableFilter: true,
        enableSorting: true,
        ready: onGridReady,
        rowData: $rootScope.players,
        rowSelection: 'multiple',
//        rowSelected: rowSelected,
        selectionChanged: selectionChange,
        suppressRowClickSelection: true,

    };

    function onGridReady() {
        // resize the columns to fit the container
        $rootScope.gridOptions.api.sizeColumnsToFit();
        // if any players have been selected, copy the array of ids and re-select them
        // otherwise use ids from retrieved nominations (if there are any)
        var ids = [];
        if ($rootScope.selectedPlayerIds && $rootScope.selectedPlayerIds.length > 0) {
            console.log("onGridReady: $rootScope.selectedPlayerIds = " + JSON.stringify($rootScope.selectedPlayerIds));
            ids = $rootScope.selectedPlayerIds.slice()
        } else if (userNoms.length > 0) {
            console.log("onGridReady: userNoms = " + JSON.stringify(userNoms));
            angular.forEach(userNoms, function(value) {
                ids.push(value.player);
            });
        } else {
            console.log("review logic");
        }

        console.log("ids: " + ids);
        if (ids.length > 0) {
            $rootScope.gridOptions.api.forEachInMemory(function (node) {
                if (ids.indexOf(node.data.id) != -1) {
                    $rootScope.gridOptions.api.selectNode(node, true);
                }
            });
        }
        // initialize the selection
        selectionChange();
    };

//    function selectionComparator(_value1, _value2, data1, data2, isInverted) {
//        return value1 - value2;
//    }


//    function rowSelected(row) {
//        window.alert("row " + row.id + " selected: " + row.player);
//    }

    $rootScope.selectedPlayerIdsOld = [];

    function selectionChange() {
//        console.log("selectionChange() called...");
        $rootScope.selectedPlayers = $rootScope.gridOptions.selectedRows;
        $rootScope.selectedPlayerIds = [];

        angular.forEach($rootScope.gridOptions.selectedRows, function(value, key) {
            $rootScope.selectedPlayerIds.push(value.id);
        });

        setSelectionCounts();
        compareWithPreviousSelection();

//        console.log("$rootScope.gridOptions.selectedNodesById = " + JSON.stringify($rootScope.gridOptions.selectedNodesById, null, 4));
    };

    function setSelectionCounts() {
        $rootScope.selectedPlayerCounts = {
            gkp: 0,
            def: 0,
            mid: 0,
            str: 0,
        };
        angular.forEach($rootScope.selectedPlayers, function (value, key) {
            if (value.position == 'GKP') {
                $rootScope.selectedPlayerCounts.gkp++;
            } else if (value.position == 'DEF') {
                $rootScope.selectedPlayerCounts.def++;
            } else if (value.position == 'MID') {
                $rootScope.selectedPlayerCounts.mid++;
            } else {
                $rootScope.selectedPlayerCounts.str++;
            }
        });
    }

    function compareWithPreviousSelection() {
//        console.log("compareWithPreviousSelection() method called...");
        if ($rootScope.selectedPlayerIds.length > $scope.selectedPlayerIdsOld.length) {
            // a new row has been selected - do nothing
//            console.log("compareWithPreviousSelection: new length > old");
        } else {
//            console.log("compareWithPreviousSelection: finding player that has been unchecked");
            angular.forEach($scope.selectedPlayerIdsOld, function (id) {
//                console.log("checking old id = " + id + " in new list");
                // find the player that has been unchecked
                if ($rootScope.selectedPlayerIds.indexOf(id) == -1) {
                    // check whether a nomination has been saved for the player...
//                    console.log("old player " + id + " not found in new list. Checking for saved nomination.");
                    var isNominated = false;
                    angular.forEach(userNoms, function(nomination) {
//                        console.log("checking old id = " + id + " against nomination: " + nomination.player);
                        if (nomination.player == id) {
//                            console.log("A nomination for player id" + nomination.player + " has been found");
                            window.alert("A nomination for player id " + nomination.player +
                                " has been saved to the database previously. \nPlease go to the preview screen and use the delete option to remove.");
                            isNominated = true;
                        }
                    });
                    if (isNominated) {
                        // ...if so, re-select the row
                        $rootScope.gridOptions.api.forEachInMemory(function (node) {
                            if (node.data.id == id) {
                                $rootScope.gridOptions.api.selectNode(node, true);
                                return;
                            }
                        });
                    }
                }
            });
        }
        // finally, update the old selected id list
        $scope.selectedPlayerIdsOld = $rootScope.selectedPlayerIds.slice()
    }

    // set the options for the position filter button group and a default value
    $scope.filter = {
        options: ['All', 'GKP', 'DEF', 'MID', 'STR'],
        radioModel: 'All',
    }

    $scope.filterOnPosition = function(position) {
        var filterApi = $rootScope.gridOptions.api.getFilterApi('position');
        if (position == 'All') {
            filterApi.selectEverything();
        } else {
            filterApi.selectNothing();
            filterApi.selectValue(position);
        }
        $rootScope.gridOptions.api.onFilterChanged();
    };


    $scope.previewNominations = function() {
        $location.path($rootScope.baseUrl + 'selection/');
    };


    $scope.previewAuctionNominations = function() {
        console.log("AuctionListController: trying: " + $rootScope.baseUrl + 'auction/selection/');
        $location.path($rootScope.baseUrl + 'auction/selection/');
    };

}]);

footyApp.controller('AuctionSummaryController', ['$scope', '$location', '$rootScope', 'AuctionNominations', 'userNoms', 'TEMPLATE_PATH', function($scope, $location, $rootScope, AuctionNominations, userNoms, TEMPLATE_PATH) {

    // URL: /players/auction/summary/
    // Main interactive player table with added column for nominating managers (anonymised when only 2 are in for a player)

    // dynamically assign templateUrls according to AuthUser
    $scope.getTemplateUrl = function() {
        if ($rootScope.authUser == 'Admin' || $rootScope.authUser == 'admin') {
            return TEMPLATE_PATH + 'main-panel/players/admin_players_auction.html';
        } else {
            return TEMPLATE_PATH + 'main-panel/players/players_auction_summary.html';
        }
    };

    // if the browser is refreshed on the player list url, redirect to baseUrl to reload the player list
    if ($rootScope.players == undefined) {
        $location.path('/players/');
    }

    var columnDefs = [
        {headerName: "Code", field: "code", width: 50},
        {headerName: "Position", field: "position", width: 60},
        {headerName: "Player", field: "name", width: 100, suppressMenu: true},
        {headerName: "Team", field: "prem_team", width: 50},
        {headerName: "Value", field: "value", width: 50, suppressMenu: true},
        {headerName: "pts", field: "last_years_total", width: 50, suppressMenu: true},
        {headerName: "Manager", field: "manager", width: 50},
        {headerName: "Nominating Managers", field: "auction_nomination_managers", width: 220},
    ];

    $rootScope.gridOptions = {
        columnDefs: columnDefs,
        enableFilter: true,
        enableSorting: true,
        ready: onGridReady,
        rowData: $rootScope.players,
        rowSelection: 'multiple',
//        rowSelected: rowSelected,
        suppressRowClickSelection: true,

    };

//    function rowSelected(row) {
//        window.alert("row " + row.id + " selected: " + row.player);
//    }

    function onGridReady() {
        // resize the columns to fit the container
        $rootScope.gridOptions.api.sizeColumnsToFit();
        var ids = [];
        if ($rootScope.selectedPlayerIds && $rootScope.selectedPlayerIds.length > 0) {
            console.log("onGridReady: $rootScope.selectedPlayerIds = " + JSON.stringify($rootScope.selectedPlayerIds));
            ids = $rootScope.selectedPlayerIds.slice()
        } else if (userNoms.length > 0) {
            console.log("onGridReady: userNoms = " + JSON.stringify(userNoms));
            angular.forEach(userNoms, function(value) {
                ids.push(value.player);
            });
        } else {
            console.log("review logic");
        }

        console.log("ids: " + ids);
        if (ids.length > 0) {
            $rootScope.gridOptions.api.forEachInMemory(function (node) {
                if (ids.indexOf(node.data.id) != -1) {
                    $rootScope.gridOptions.api.selectNode(node, true);
                }
            });
        }
        // initialize the selection
        selectionChange();
    };

    $rootScope.selectedPlayerIdsOld = [];

    function selectionChange() {
//        console.log("selectionChange() called...");
        $rootScope.selectedPlayers = $rootScope.gridOptions.selectedRows;
        $rootScope.selectedPlayerIds = [];

        angular.forEach($rootScope.gridOptions.selectedRows, function(value, key) {
            $rootScope.selectedPlayerIds.push(value.id);
        });

        setSelectionCounts();
        compareWithPreviousSelection();

//        console.log("$rootScope.gridOptions.selectedNodesById = " + JSON.stringify($rootScope.gridOptions.selectedNodesById, null, 4));
    };

    function setSelectionCounts() {
        $rootScope.selectedPlayerCounts = {
            gkp: 0,
            def: 0,
            mid: 0,
            str: 0,
        };
        angular.forEach($rootScope.selectedPlayers, function (value, key) {
            if (value.position == 'GKP') {
                $rootScope.selectedPlayerCounts.gkp++;
            } else if (value.position == 'DEF') {
                $rootScope.selectedPlayerCounts.def++;
            } else if (value.position == 'MID') {
                $rootScope.selectedPlayerCounts.mid++;
            } else {
                $rootScope.selectedPlayerCounts.str++;
            }
        });
    }

    function compareWithPreviousSelection() {
//        console.log("compareWithPreviousSelection() method called...");
        if ($rootScope.selectedPlayerIds.length > $scope.selectedPlayerIdsOld.length) {
            // a new row has been selected - do nothing
//            console.log("compareWithPreviousSelection: new length > old");
        } else {
//            console.log("compareWithPreviousSelection: finding player that has been unchecked");
            angular.forEach($scope.selectedPlayerIdsOld, function (id) {
//                console.log("checking old id = " + id + " in new list");
                // find the player that has been unchecked
                if ($rootScope.selectedPlayerIds.indexOf(id) == -1) {
                    // check whether a nomination has been saved for the player...
//                    console.log("old player " + id + " not found in new list. Checking for saved nomination.");
                    var isNominated = false;
                    angular.forEach(userNoms, function(nomination) {
//                        console.log("checking old id = " + id + " against nomination: " + nomination.player);
                        if (nomination.player == id) {
//                            console.log("A nomination for player id" + nomination.player + " has been found");
                            window.alert("A nomination for player id " + nomination.player +
                                " has been saved to the database previously. \nPlease go to the preview screen and use the delete option to remove.");
                            isNominated = true;
                        }
                    });
                    if (isNominated) {
                        // ...if so, re-select the row
                        $rootScope.gridOptions.api.forEachInMemory(function (node) {
                            if (node.data.id == id) {
                                $rootScope.gridOptions.api.selectNode(node, true);
                                return;
                            }
                        });
                    }
                }
            });
        }
        // finally, update the old selected id list
        $scope.selectedPlayerIdsOld = $rootScope.selectedPlayerIds.slice()
    }

    // set the options for the position filter button group and a default value
    $scope.filter = {
        options: ['All', 'GKP', 'DEF', 'MID', 'STR'],
        radioModel: 'All',
    }

    $scope.filterOnPosition = function(position) {
        var filterApi = $rootScope.gridOptions.api.getFilterApi('position');
        if (position == 'All') {
            filterApi.selectEverything();
        } else {
            filterApi.selectNothing();
            filterApi.selectValue(position);
        }
        $rootScope.gridOptions.api.onFilterChanged();
    };

    $scope.previewAuctionNominations = function() {
        console.log("AuctionSummaryController: trying: " + $rootScope.baseUrl + 'auction/selection/');
        $location.path($rootScope.baseUrl + 'auction/selection/');
    };

}]);


footyApp.controller('AuctionSelectionController', ['$scope', '$rootScope', '$location', '$modal', 'AuctionNominations', 'userNoms', 'currentWindow', function($scope, $rootScope, $location, $modal, AuctionNominations, userNoms, currentWindow) {

    // validation
    $scope.validateNominations = function() {
         console.log("validateNominations(): warnings = " + $rootScope.warnings);
        $rootScope.errors = [];
        $rootScope.warnings = [];

        var counts = $rootScope.selectedPlayerCounts;
        var gkpDiff = $rootScope.constants.AUCTION_GKP - counts.gkp,
            defDiff = $rootScope.constants.AUCTION_DEF - counts.def,
            midDiff = $rootScope.constants.AUCTION_MID - counts.mid,
            strDiff = $rootScope.constants.AUCTION_STR - counts.str;

        console.log("validateNominations(): diffs = " + gkpDiff + ", " +  defDiff + ", " + midDiff + ", " + strDiff);

        if (gkpDiff > 0) {
            $rootScope.warnings.push("You can nominate " + gkpDiff + " more goalkeeper(s).");
        } else if (gkpDiff < 0) {
            $rootScope.errors.push("You need to delete " + Math.abs(gkpDiff) + " goalkeeper nomination(s).");
        }

        if (defDiff > 0) {
            $rootScope.warnings.push("You can nominate " + defDiff + " more defender(s).");
        } else if (defDiff < 0) {
            $rootScope.errors.push("You need to delete " + Math.abs(defDiff) + " defender nomination(s).");
        }

        if (midDiff > 0) {
            $rootScope.warnings.push("You can nominate " + midDiff + " more midfielder(s).");
        } else if (midDiff < 0) {
            $rootScope.errors.push("You need to delete " + Math.abs(midDiff) + " midfielder nomination(s).");
        }

        if (strDiff > 0) {
            $rootScope.warnings.push("You can nominate " + strDiff + " more striker(s).");
        } else if (strDiff < 0) {
            $rootScope.errors.push("You need to delete " + Math.abs(strDiff) + " striker nomination(s).");
        }

//        console.log("validateNominations(): warnings = " + $rootScope.warnings);
//        console.log("validateNominations(): errors = " + $rootScope.errors);
    };

    $scope.validateNominations();

    $scope.deleteNomination = function(player) {
//        console.log("deleteNomination(): player = " + JSON.stringify(player));
        var index = $rootScope.selectedPlayers.indexOf(player)
//        console.log('deleteNomination: index = ' + index)
        if (index != -1) {
            // remove from selectedPlayers & Ids arrays
            $rootScope.selectedPlayers.splice(index, 1);
            $rootScope.selectedPlayerIds.splice(index, 1);
//            console.log("deleteNomination(): after splice: selectedPlayers = " + JSON.stringify($rootScope.selectedPlayers));
            if (player.position == 'GKP') {
                $rootScope.selectedPlayerCounts.gkp--;
            } else if (player.position == 'DEF') {
                $rootScope.selectedPlayerCounts.def--;
            } else if (player.position == 'MID') {
                $rootScope.selectedPlayerCounts.mid--;
            } else {
                $rootScope.selectedPlayerCounts.str--;
            }
        }

        $scope.validateNominations()

        // delete from the database (if there is a record present)
        var nom_id
        console.log("deleteNomination(): userNoms = " + JSON.stringify(userNoms));
        angular.forEach(userNoms, function(nomination) {
            if (nomination.player == player.id) {
                console.log("deleteNomination(): matching nomination.player = " + nomination.player);
                nom_id = nomination.id;
            }
        });
        if (nom_id) {
            AuctionNominations.remove({id: nom_id}).$promise
                .then(function(response) {
                    console.log('deleteNomination: response: ' + JSON.stringify(response));
    //                setSelectionCounts();
                }, function(error) {
                    console.log('deleteNomination: error: ' + JSON.stringify(error));
                });
        }
    }

    $scope.saveNominations = function() {

        // TODO - check currentWindow.type here

        var saveErrors = 0;

        angular.forEach($rootScope.selectedPlayers, function(player) {
            var nominationExists = false;
            for (i = 0; i < userNoms.length; i++) {
                if (userNoms[i].player == player.id) {
                    console.log("A nomination has been previously saved for player " + player.id + ", exiting for loop...");
                    nominationExists = true;
                    break;
                }
            }

            if (!nominationExists) {
                AuctionNominations.save({player: player.id, team: $rootScope.userTeam.id}).$promise
                    .then(function(response) {
                        console.log('saveNomination: response: ' + JSON.stringify(response));
                    }, function(error) {
                        console.log('saveNomination: error: ' + JSON.stringify(error));
                        saveErrors += 1;
                    });
            }

        });

        if (saveErrors > 0) {
            var modalInstance = $modal.open({
                templateUrl: 'errorModal.html',
                controller: 'ModalErrorControl',
                size: 's',
                resolve: {
                    error: function() {
                        return {
                            title: 'Error saving nominations',
                            message: "An error occurred for " + saveErrors + " nominations.  The player list will be reloaded please try again.\nIf you've seen this before then don't panic and drop Dan an email."
                        };
                    }
                },
            });
            modalInstance.result.then(function (result) {
                $location.path('/transfers/');
            }, function () {
                $location.path('/transfers/');
            });

        } else {
            console.log("saveNominations(): no errors!");
            var modalInstance = $modal.open({
                templateUrl: 'messageModal.html',
                controller: 'ConfirmOperationController',
//                size: 'sm',
                resolve: {
                    modal: function () { return {message: 'A total of ' + $rootScope.selectedPlayers.length + ' player nominations have been successfully saved.\nFurther changes can be made up until the deadline.'}; },
                }
            });
        };
	};

	$scope.ok = function () {
    	var response = Slugify.post({title: $scope.page.title},
    		function() {
    			$scope.page.link = response.link;
      			$modalInstance.close($scope.page);
    		},
			function (response) {
				$scope.error_message = response.data.error_message;
			}
		);
  	};

  	$scope.cancel = function () {
    	$modalInstance.dismiss('cancel');
  	};

}]);

footyApp.controller('AuctionNominationsController', ['$scope', '$location', '$rootScope', '$filter', 'AuctionNominations', 'userNoms', 'TEMPLATE_PATH', function($scope, $location, $rootScope, $filter, AuctionNominations, userNoms, TEMPLATE_PATH) {

    $scope.players = $rootScope.players;

    $scope.userNoms = userNoms;

    $scope.isAdmin = ($rootScope.authUser == 'Admin');

    $scope.isManagerView = false;

    $scope.toggleIsManagerView = function() {
        $scope.isManagerView = !$scope.isManagerView

        if ($scope.isManagerView) {
            $scope.players = $filter('filter')($rootScope.players, function(player, index, array) {
                return player.auction_nomination_managers.indexOf($rootScope.authUser) != -1;
            }, true);
        } else {
            $scope.players = $rootScope.players;
        }
    };

}]);

footyApp.controller('AdminAuctionTeamsController', ['$scope', '$location', '$rootScope', '$filter', 'Players', 'teams', 'auctionTeamSummary', 'auctionRandomPlayerCodes', 'TEMPLATE_PATH', function($scope, $location, $rootScope, $filter, Players, teams, auctionTeamSummary, auctionRandomPlayerCodes, TEMPLATE_PATH) {

    $scope.players = $rootScope.players;
    $scope.auctionTeamSummary = auctionTeamSummary;
    $scope.randomPlayerCodes = auctionRandomPlayerCodes;
    $scope.teams = teams;

    console.log("auctionTeamSummary: " + JSON.stringify(auctionTeamSummary, null, 4));

    $scope.isAdmin = ($rootScope.authUser == 'Admin');

    $scope.selectedPlayer = {};

    $scope.getPlayer = function(playerCode) {
        console.log("get_player");

        // if no player code is provide, use the next one from the randomised list
        if (playerCode == undefined) {
            playerCode = $scope.randomPlayerCodes.pop();
            console.log("playerCode set to " + playerCode);
            console.log("randomPlayerCodes = " + JSON.stringify($scope.randomPlayerCodes))

        }

        Players.query({code: playerCode}).$promise
            .then(function (response) {
                console.log("getPlayer(): response = " + JSON.stringify(response));
                // returns an array with one player object
                $scope.selectedPlayer = response[0];
            },
            function (error) {
                window.alert(JSON.stringify(error));
            });
    };

//    $scope.getRandomPlayer = function() {
//        return $scope.getPlayer($scope.randomPlayerCodes.pop());
//    };

    $scope.savePlayer = function() {
        var p = $scope.selectedPlayer;
        var position = p.position[0]
        console.log("savePlayers: " + JSON.stringify(p, null, 4));

        Players.patch(p).$promise
            .then(function (response) {
                $scope.auctionTeamSummary[p.team].players[position].push(p.sale)
                $scope.auctionTeamSummary[p.team].funds -= p.sale;
                $scope.selectedPlayer = {};
            },
            function (error) {
                window.alert(JSON.stringify(error));
            });
    };

    $scope.setManager = function(manager) {
        angular.forEach($scope.teams, function(team, id) {
            if (team.manager.username === manager) {
                $scope.selectedPlayer.team = team.id;
            }
        });
    }

    $scope.cancel = function() {
        $scope.selectedPlayer = {};
    };

}]);

//footyApp.filter('byActionName', function() {
//	return function(tasks, action_names) {
//		var out = tasks.filter(function( task ) {
//
//  			angular.forEach(action_names, function(name, key) {
//				console.log('workflowFilters: by_action_name: forEach loop value: name: ' + name);
//				if (task.node.name == name) {
//					return true;
//				};
//			});
//
//  			// return task.node.name == 'Finalise Hit Rtp' ||
//  				// task.node.name == 'Request Computational Model';
//		});
//		// Filter logic here, adding matches to the out var.
//		return out;
//	};
//});

footyApp.controller('TransferListController', ['$scope', '$location', '$rootScope', 'CurrentWindow', 'TransferNominations', 'userTransferNoms', 'TEMPLATE_PATH', function($scope, $location, $rootScope, CurrentWindow, TransferNominations, userTransferNoms, TEMPLATE_PATH) {

    CurrentWindow.query().$promise
        .then(function(response) {
            $scope.currentWindow = response;
            console.log("TransferListController: $scope.currentWindow = " + JSON.stringify($scope.currentWindow));
        });

    // if the browser is refreshed on the player list url, redirect to baseUrl to reload the player list
    if ($rootScope.players == undefined) {
        $location.path('/transfers/');
    }

    var columnDefs = [
        {headerName: "Code", field: "code", width: 60},
        {headerName: "Position", field: "position", width: 60},
        {headerName: "Player", field: "name", width: 100, suppressMenu: true},
        {headerName: "Team", field: "prem_team", width: 60},
        {headerName: "Value", field: "value", width: 60, suppressMenu: true},
        {headerName: "Sale", field: "sale", width: 60, suppressMenu: true},
        {headerName: "Manager", field: "manager", width: 100},
        {headerName: "pts", field: "total_score", width: 60, suppressMenu: true},
        {headerName: "Select", field: null, width: 60, checkboxSelection: true},  //, comparator: selectionComparator
    ];

    $rootScope.gridOptions = {
        columnDefs: columnDefs,
        enableFilter: true,
        enableSorting: true,
        ready: onGridReady,
        rowData: $rootScope.players,
        rowSelection: 'multiple',
//        rowSelected: rowSelected,
        selectionChanged: selectionChange,
        suppressRowClickSelection: true,

    };

    function rowSelected(row) {
        if (row.manager != null) {
            window.alert("");
        }
    };

    function onGridReady() {
        // resize the columns to fit the container
        $rootScope.gridOptions.api.sizeColumnsToFit();
        // if any players have been selected, copy the array of ids and re-select them
        // otherwise use ids from retrieved nominations (if there are any)
        var ids = [];
        if ($rootScope.selectedPlayerIds && $rootScope.selectedPlayerIds.length > 0) {
            console.log("onGridReady: $rootScope.selectedPlayerIds = " + JSON.stringify($rootScope.selectedPlayerIds));
            ids = $rootScope.selectedPlayerIds.slice()
        } else if (userTransferNoms.length > 0) {
            console.log("onGridReady: userTransferNoms = " + JSON.stringify(userTransferNoms));
            angular.forEach(userTransferNoms, function(value) {
                ids.push(value.player);
            });
        } else {
            console.log("review logic");
        }

        console.log("ids: " + ids);
        if (ids.length > 0) {
            $rootScope.gridOptions.api.forEachInMemory(function (node) {
                if (ids.indexOf(node.data.id) != -1) {
                    $rootScope.gridOptions.api.selectNode(node, true);
                }
            });
        }
        // initialize the selection
        selectionChange();
    };

    $rootScope.selectedPlayerIdsOld = [];

    function selectionChange() {
//        console.log("selectionChange() called...");

        $rootScope.selectedPlayers = $rootScope.gridOptions.selectedRows;
        $rootScope.selectedPlayerIds = [];

        angular.forEach($rootScope.gridOptions.selectedRows, function(value, key) {
            // if the player is already in a team then deselect it
            if (value.manager != null) {
                $rootScope.gridOptions.api.forEachInMemory(function(node) {
                    if (node.data.id == value.id) {
                        console.log("Deselecting row: " + node.data.name);
                        $rootScope.gridOptions.api.deselectNode(node);
                        return;
                    }
                });
            } else {
                $rootScope.selectedPlayerIds.push(value.id);
            }
        });

//        setSelectionCounts();
        compareWithPreviousSelection();

//        console.log("$rootScope.gridOptions.selectedNodesById = " + JSON.stringify($rootScope.gridOptions.selectedNodesById, null, 4));
    };

    function compareWithPreviousSelection() {
//        console.log("compareWithPreviousSelection() method called...");
        if ($rootScope.selectedPlayerIds.length > $scope.selectedPlayerIdsOld.length) {
            // a new row has been selected - uncheck it if the player is already bought
//            console.log("compareWithPreviousSelection: new length > old");
        } else {
//            console.log("compareWithPreviousSelection: finding player that has been unchecked");
            angular.forEach($scope.selectedPlayerIdsOld, function(id) {
//                console.log("checking old id = " + id + " in new list");
                // find the player that has been unchecked
                if ($rootScope.selectedPlayerIds.indexOf(id) == -1) {
                    // check whether a nomination has been saved for the player...
//                    console.log("old player " + id + " not found in new list. Checking for saved nomination.");
                    var isNominated = false;
                    angular.forEach(userTransferNoms, function(nomination) {
//                        console.log("checking old id = " + id + " against nomination: " + nomination.player);
                        if (nomination.player == id) {
//                            console.log("A nomination for player id" + nomination.player + " has been found");
                            window.alert("A nomination for player id " + nomination.player +
                                " has been saved to the database previously. \nPlease go to the preview screen and use the delete option to remove.");
                            isNominated = true;
                        }
                    });
                    if (isNominated) {
                        // ...if so, re-select the row
                        $rootScope.gridOptions.api.forEachInMemory(function (node) {
                            if (node.data.id == id) {
                                $rootScope.gridOptions.api.selectNode(node, true);
                                return;
                            }
                        });
                    }
                }
            });
        }
        // finally, update the old selected id list
        $scope.selectedPlayerIdsOld = $rootScope.selectedPlayerIds.slice()
    }

    // set the options for the position filter button group and a default value
    $scope.filter = {
        options: ['All', 'GKP', 'DEF', 'MID', 'STR'],
        radioModel: 'All',
    }

    $scope.filterOnPosition = function(position) {
        var filterApi = $rootScope.gridOptions.api.getFilterApi('position');
        if (position == 'All') {
            filterApi.selectEverything();
        } else {
            filterApi.selectNothing();
            filterApi.selectValue(position);
        }
        $rootScope.gridOptions.api.onFilterChanged();
    };


    $scope.previewNominations = function() {
        console.log("$rootScope.baseUrl = " + $rootScope.baseUrl);
        $location.path($rootScope.baseUrl + 'selection/');
    };

    $scope.previewAuctionNominations = function() {
        console.log("TransferListController: trying: " + $rootScope.baseUrl + 'auction/selection/');
        $location.path($rootScope.baseUrl + 'auction/selection/');
    };

}]);

footyApp.controller('TransferSelectionController', ['$scope', '$rootScope', '$location', '$modal', 'CurrentWindow', 'TransferNominations', 'userTransferNoms', function($scope, $rootScope, $location, $modal, CurrentWindow, TransferNominations, userTransferNoms) {

    CurrentWindow.query().$promise
        .then(function(response) {
            $scope.currentWindow = response;
            console.log("TransferSelectionController: $scope.currentWindow = " + JSON.stringify($scope.currentWindow));
        });

    $scope.transferNomsDict = {};

    $scope.playerNoms = [];

    console.log("TransferSelectionController: initializing...");

    // create a lookup dict of nominations based on player id as key
    angular.forEach(userTransferNoms, function(value, key) {
        console.log("userTransferNoms: key: " + JSON.stringify(key) + "; value: " + JSON.stringify(value))
//        $scope.transferNomsDict[value.player] = value;

        // cast the bid to a float
        value.bid = parseFloat(value.bid);
        value.id = parseInt(value.id);

        var player = $rootScope.selectedPlayers.filter(function( obj ) {
          return obj.id == value.player;
        })[0];
        console.log("found existing nomination for player: " + JSON.stringify(player));
        $scope.playerNoms.push({nom: value, player: player});
    });

//    console.log("$scope.transferNomsDict = " + $scope.transferNomsDict, null, 4);

    angular.forEach($rootScope.selectedPlayers, function(player, key) {
            console.log("selectedPlayers: key: " + JSON.stringify(key) + "; player: " + JSON.stringify(player))
            var noms = $scope.playerNoms.filter(function(nom) {
                console.log("nom.player.id = " + nom.player.id + " : "+ typeof nom.player.id)
                console.log("player.id = " + player.id + " : "+ typeof player.id)
                return nom.player.id == player.id;
            });

            console.log("noms = " + JSON.stringify(noms));

            if (noms.length == 0) {
                var nom = {player: player.id, bid: undefined, id: undefined, team: $rootScope.userTeam.id}
                $scope.playerNoms.push({nom: nom, player: player});
            }


        });


    // validation
    $scope.validateNominations = function() {
        console.log("validateNominations(): errors = " + $rootScope.errors);
        $rootScope.errors = [];

        angular.forEach($scope.selectedPlayers, function(player, key) {
            console.log("selectedPlayers: key: " + JSON.stringify(key) + "; player: " + JSON.stringify(player))
            var noms = $scope.playerNoms.filter(function(nom) {
                return nom.player.id = player.id;
            });

            if (noms.length == 0) {
                var nom = {player: player.id, bid: undefined, id: undefined, team: $rootScope.userTeam.id}
                $scope.playerNoms.push({nom: nom, player: player});
            }


        });

    };

    $scope.deleteNomination = function(playerNom) {
        console.log("deleteNomination(): playerNom = " + JSON.stringify(playerNom));

        if (playerNom.nom.id != undefined) {
            TransferNominations.remove({id: playerNom.nom.id}).$promise
                .then(function(response) {
                    console.log('deleteNomination: response: ' + JSON.stringify(response));
                }, function(error) {
                    console.log('deleteNomination: error: ' + JSON.stringify(error));
                });
        }

        // remove from the player nominations
        var index = $scope.playerNoms.indexOf(playerNom)
        if (index > -1) {
            $scope.playerNoms.splice(index, 1);
        }

        var playerIndex = $rootScope.selectedPlayers.indexOf(playerNom.player)
        console.log('delete from selectedPlayers: playerIndex = ' + playerIndex)
        if (playerIndex != -1) {
            // remove from selectedPlayers & Ids arrays
            $rootScope.selectedPlayers.splice(playerIndex, 1);
            $rootScope.selectedPlayerIds.splice(playerIndex, 1);
        }

    }

    $scope.duplicateNomination = function(playerNom) {
        var index = $scope.playerNoms.indexOf(playerNom);
        var nom = {player: playerNom.player.id, bid: undefined, id: undefined, team: $rootScope.userTeam.id}
        var duplicate = {nom: nom, player: playerNom.player};

        console.log("duplicateNominations: duplicate = " + JSON.stringify(duplicate));
        $scope.playerNoms.splice(index + 1, 0, duplicate);
        console.log("playerNoms.length = " + $scope.playerNoms.length);
    }

    $scope.saveNominations = function() {

        var saveErrors = 0;

        angular.forEach($scope.playerNoms, function(playerNom) {

            console.log("saving playerNom = " + JSON.stringify(playerNom));

            if (playerNom.nom.id != undefined) {
                console.log("A nomination has been previously saved for player " + playerNom.player.id + ", exiting for loop...");
                TransferNominations.patch({id: playerNom.nom.id, player: playerNom.player.id, team: $rootScope.userTeam.id, bid: playerNom.nom.bid}).$promise
                .then(function(response) {
                    console.log('saveNomination: patch response: ' + JSON.stringify(response));
                }, function(error) {
                    console.log('saveNomination: patch error: ' + JSON.stringify(error));
                    saveErrors += 1;
                });
            } else {
                TransferNominations.save(playerNom.nom).$promise
                    .then(function(response) {
                        console.log('saveNomination: response: ' + JSON.stringify(response));
                    }, function(error) {
                        console.log('saveNomination: error: ' + JSON.stringify(error));
                        saveErrors += 1;
                    });

            }
        });

        if (saveErrors > 0) {
            var modalInstance = $modal.open({
                templateUrl: 'errorModal.html',
                controller: 'ModalErrorControl',
                size: 's',
                resolve: {
                    error: function() {
                        return {
                            title: 'Error saving nominations',
                            message: "An error occurred for " + saveErrors + " nominations.  The player list will be reloaded please try again.\nIf you've seen this before then don't panic and drop Dan an email."
                        };
                    }
                },
            });
            modalInstance.result.then(function (result) {
                $location.path('/players/');
            }, function () {
                $location.path('/players/');
            });

        } else {
            console.log("saveNominations(): no errors!");
            var modalInstance = $modal.open({
                templateUrl: 'messageModal.html',
                controller: 'ConfirmOperationController',
//                size: 'sm',
                resolve: {
                    modal: function () { return {message: 'A total of ' + $scope.playerNoms.length + ' player nominations have been successfully saved.\nFurther changes can be made up until the deadline.'}; },
                }
            });
        };
	};


	$scope.ok = function () {
    	var response = Slugify.post({title: $scope.page.title},
    		function() {
    			$scope.page.link = response.link;
      			$modalInstance.close($scope.page);
    		},
			function (response) {
				$scope.error_message = response.data.error_message;
			}
		);
  	};

  	$scope.cancel = function () {
    	$modalInstance.dismiss('cancel');
  	};

}]);

footyApp.controller('TransferRedirectController', ['$scope', '$rootScope', '$location', 'players', 'currentWindow', function($scope, $rootScope, $location, players, currentWindow) {

    $rootScope.players = players;
    $rootScope.baseUrl = $location.path();

    console.log("TransferRedirectController: currentWindow = " + JSON.stringify($scope.currentWindow));
    var windowTypes = $rootScope.windowTypes;

    if (currentWindow.type == windowTypes.TRANSFER_NOMINATION) {
        console.log("TransferRedirectController: redirecting to /transfers/players_list/");
        $location.path('/transfers/players_list/');
    } else if (currentWindow.type == windowTypes.TRANSFER_CONFIRMATION) {
        console.log("TransferRedirectController: redirecting to /transfers/confirmation/");
        $location.path('/transfers/confirmation/');
    } else {
        console.log("TransferRedirectController: redirecting to /transfers/summary/");
        $location.path('/transfers/summary/');
    }

}]);

footyApp.controller('TransferSummaryController', ['$scope', '$rootScope', '$location', '$modal', 'CurrentWindow', 'TransferNominations', 'transferNominationSummary', 'TransferNominationSummary', function($scope, $rootScope, $location, $modal, CurrentWindow, TransferNominations, transferNominationSummary, TransferNominationSummary) {

    CurrentWindow.query().$promise
        .then(function(response) {
            $scope.currentWindow = response;
            console.log("TransferSummaryController: $scope.currentWindow = " + JSON.stringify($scope.currentWindow));
            if ($scope.currentWindow == $rootScope.windowTypes.TRANSFER_NOMINATION) {
                $location.path("/transfers/");
            }
        });

    $scope.allNominations = transferNominationSummary;
    console.log("$scope.allNominations: " + $scope.allNominations);

    $scope.refreshData = function() {
        TransferNominationSummary.query().$promise
            .then(function(response) {
                console.log('TransferNominationSummary: response = ' + JSON.stringify(response));
                $scope.allNominations = response;
            });
    };

    $scope.refreshData();

}]);

footyApp.controller('TransferConfirmationController', ['$scope', '$rootScope', '$location', '$route', '$modal', 'CurrentWindow', 'TransferNominations', 'AcceptBid', 'PassOnBid', 'ReturnPlayerToPool', 'ProcessTransfersForTeam', 'TransferNominationPlayerDetails', 'TeamDetails', function($scope, $rootScope, $location, $route, $modal, CurrentWindow, TransferNominations, AcceptBid, PassOnBid, ReturnPlayerToPool, ProcessTransfersForTeam, TransferNominationPlayerDetails, TeamDetails) {

//    $scope.userNominations = userNominationDetails.nominations;
//    console.log("TransferConfirmationController: $scope.userNominations = " + JSON.stringify($scope.userNominations, null, 4));
//    $scope.playerDetails = userNominationDetails.players
//    console.log("TransferConfirmationController: $scope.playerDetails = " + JSON.stringify($scope.playerDetails, null, 4));
//    $scope.teamDetails = teamDetails;
//    console.log("TransferConfirmationController: $scope.teamDetails = " + JSON.stringify($scope.teamDetails, null, 4));

    CurrentWindow.query().$promise
        .then(function(response) {
            $scope.currentWindow = response;
            console.log("TransferConfirmationController: $scope.currentWindow = " + JSON.stringify($scope.currentWindow));
        });


    $scope.userNominations = {};
    $scope.playerDetails = {};
    $scope.teamDetails = {};
    $scope.playersToSell = [];
    $scope.playerToSell = undefined;
    $scope.funds = 0;


    $scope.refreshData = function() {
        TransferNominationPlayerDetails.query().$promise
            .then(function(response) {
                console.log('TransferNominationPlayerDetails: response = ' + JSON.stringify(response));
                $scope.userNominations = response.nominations;
                $scope.userNominations.disableFinalise = updateDisableFinalise();
                $scope.playerDetails = response.players;

            });

        TeamDetails.get({id: $rootScope.userTeam.id}).$promise
            .then(function(response) {
                console.log('TeamDetails: response = ' + JSON.stringify(response));
                $scope.teamDetails = response;
//                angular.forEach($scope.playersToSell, function (player, id) {
//                    $scope.teamDetails.funds = parseFloatAddAndRound(player.value, $scope.teamDetails.funds);
//                });
                updateFunds()
            });
    };

    // Load the initial data.
    $scope.refreshData();

    $scope.acceptNomination = function(nomination) {
        console.log("acceptNomination(): nomination.id = " + JSON.stringify(nomination.id));
        AcceptBid.patch({id: nomination.id}).$promise
            .then(function(response) {
                console.log("acceptNomination(): Bid for nomination " + nomination.id + " successfully accepted.");
                $scope.refreshData();
            }, function(error) {
                console.log("acceptNomination(): error " + error.detail);
            });
    };

    $scope.passOnNomination = function(nomination) {
        console.log("passOnNomination(): nomination = " + JSON.stringify(nomination));
        PassOnBid.patch({id: nomination.id}).$promise
            .then(function(response) {
                console.log("passOnNomination(): Bid for player " + nomination.id + " was passed.");
                $scope.refreshData();
            }, function(error) {
                console.log("passOnNomination(): error " + error.detail);
            });
    };

    var parseFloatAddAndRound = function(arg1, arg2) {
        return (parseFloat(arg1) + parseFloat(arg2)).toFixed(1);
    };

    var updateFunds = function() {
        $scope.funds = parseFloat($scope.teamDetails.funds);
        angular.forEach($scope.playersToSell, function (player, id) {
            console.log("parseFloat(player.value):", parseFloat(player.value));
            $scope.funds += parseFloat(player.value);
        });
        angular.forEach($scope.userNominations, function (nomination) {
            if (nomination.status == 'Accepted') {
                $scope.funds -= parseFloat(nomination.bid);
            }
        });

        // round the calculated value
        $scope.funds = Math.round( $scope.funds * 10 ) / 10;
    };

    $scope.addPlayerToSell = function(player) {
        $scope.playersToSell.push(player);
        $scope.playerToSell = undefined;
        updateFunds();
    };

    $scope.removePlayerToSell = function(player) {
        var index = $scope.playersToSell.indexOf(player);
        if (index > -1) {
            $scope.playersToSell.splice(index, 1);
        }
        updateFunds();
    };

    $scope.messages = [];

    var updateDisableFinalise = function() {
        console.log("disableFinalise()...");
        console.log("$scope.userNominations = " + JSON.stringify($scope.userNominations));
        // if any nominations are still pending then don't allow the Finalise button to show
        // TODO - additional logic needed here??
        for (var i = 0; i < $scope.userNominations.length; i++) {
            console.log("disableFinalise(): $scope.userNominations[i].status = " + $scope.userNominations[i].status);
            if ($scope.userNominations[i].status == 'Pending') {
                return true;
            }
        }
        return false;
    };

    $scope.finaliseTransfers = function() {
        console.log("finaliseTransfers()");

//        angular.forEach($scope.playersToSell, function (player) {
//            ReturnPlayerToPool.patch({id: player.id}).$promise
//            .then(function(response) {
//                console.log("ReturnPlayerToPool(): response " + JSON.stringify(response));
//                $scope.messages.push(response.detail);
//                $scope.removePlayerToSell(player);
//                $scope.refreshData();
//            }, function(error) {
//                console.log("ReturnPlayerToPool(): error " + error.detail);
//                $scope.messages.push(error.detail);
//            });
//        });

        ProcessTransfersForTeam.get({id: $rootScope.userTeam.id}).$promise
            .then(function(response) {
                console.log("ProcessTransfersForTeam(): response = " + JSON.stringify(response));
                // extend the messages array with the messages received here
                Array.prototype.push.apply($scope.messages, response.messages);
                $scope.refreshData();
            }, function(error) {
                console.log("ProcessTransfersForTeam(): error " + JSON.stringify(error));
                $scope.messages.push(error);
            });
    };

    $scope.sellPlayer = function(player) {
        ReturnPlayerToPool.patch({id: player.id}).$promise
            .then(function(response) {
                console.log("ReturnPlayerToPool(): response " + JSON.stringify(response));
                $scope.messages.push(response.detail);
                $scope.removePlayerToSell(player);
                $scope.refreshData();
            }, function(error) {
                console.log("ReturnPlayerToPool(): error " + error.detail);
                $scope.messages.push(error.detail);
            });
    };

    $scope.editTeamLineup = function () {
        // redirect to the line-up url
        $location.path('/#/teams/' + $rootScope.userTeam.id + '/lineup/');
    };

}]);

footyApp.controller('TeamsController', ['$scope', '$rootScope', '$location', '$route', 'Teams', 'AuthUser', function ($scope, $rootScope, $location, $route, Teams, AuthUser) {

    Teams.query().$promise
        .then(function(data) {
        console.log("TeamsController: Teams.query() data = " + JSON.stringify(data));
		$rootScope.teams = data;
	});

	$scope.selectTeam = function(team) {
		$rootScope.$emit('select_team', team);
	};

	// Listener to update menu. Other controllers need to emit the signal when they want to change the space.
	$rootScope.$on('select_team', function(event, team) {
	    $rootScope.selected_team = team;
	});

	// Listener to provide the authenticated username to the rootscope, regardless of which url is linked to or refreshed
	$rootScope.$on('$routeChangeSuccess', function() {
		AuthUser.get().$promise
            .then(function (response) {
                console.log('authUser = ' + response.username);
                $rootScope.authUser = response.username;
                angular.forEach($scope.teams, function(value, key) {
                    if (value.manager.username == response.username) {
                        $rootScope.userTeam = value;
                        console.log('userTeam.name = ' + $rootScope.userTeam.name);
                    }
                });

//                UserTeam.get({user_id: response.username}).$promise
//                    .then(function (team_response) {
//                        console.log('userTeam.name = ' + team_response.name);
//                        $rootScope.userTeam = team_response
//                    });

            });
	});
}]);


footyApp.controller('ConfirmNominationsController', ['$scope', '$modalInstance', 'modal', 'warnings', 'errors', function($scope, $modalInstance, modal, warnings, errors) {
	$scope.modal = modal;
	$scope.warnings = warnings;
	$scope.errors = errors;

	$scope.ok = function() {
		$modalInstance.close('OK');
	};

	$scope.cancel = function() {
		$modalInstance.dismiss();
	};
}]);

footyApp.controller('ConfirmOperationController', ['$scope', '$modalInstance', 'modal', function($scope, $modalInstance, modal) {
	$scope.modal = modal;

	$scope.ok = function() {
		$modalInstance.close('OK');
	};

	$scope.cancel = function() {
		$modalInstance.dismiss();
	};
}]);

footyApp.controller('TeamScoresController', ['$scope', '$rootScope', '$route', '$location', '$timeout', '$modal', '$window', 'TEMPLATE_PATH', 'Players', 'TeamValidate', 'Teams', 'teamDetails', 'TeamScores', 'teamScores', 'CurrentWindow', function($scope, $rootScope, $route, $location, $timeout, $modal, $window, TEMPLATE_PATH, Players, TeamValidate, Teams, teamDetails, TeamScores, teamScores, CurrentWindow) {
    $scope.team = teamDetails;
    $scope.scores = teamScores;
    console.log("scores = " + JSON.stringify($scope.scores, null, 4));

    $scope.scores.month = new Date().getMonth();
    console.log("scores.month = " + $scope.scores.month);

    CurrentWindow.query().$promise
        .then(function(response) {
            $scope.currentWindow = response;
            console.log("TeamScoresController: $scope.currentWindow = " + JSON.stringify($scope.currentWindow));
        });

    $scope.getScore = function(player_id, week_id) {
        var score = $filter('filter')($scope.scores.player_scores, {'player': player_id, week: week_id});
        if (score == undefined || score.value == undefined) {
            return '#'
        } else if (!score.is_counted) {
            return '*' + score.value + '*';
        } else {
            return score.value;
        }

    };

    $scope.getScoresForMonth = function(month) {
        // update the team details for a specific month
        // python months are numbered from one JavaScript from zero
        TeamScores.get({id: $route.current.params.team_id, month: month + 1}).$promise
           .then(function(response) {
               console.log("getScoresForMonth: response = " + JSON.stringify(response, null, 4));
               $scope.scores = response;
               $scope.scores.month = month;
           });
    };

    var processExPlayers = function() {
        // for all ex_players change 'status' to 'A' (they may have been bought by another team, but here
        // we are only concerned with their status w.r.t this team)
        angular.forEach($scope.team.ex_players, function(player) {
            player.status = 'A';
        });
        // combine 'players' and 'ex_players' lists into one list - 'all_players'
        $scope.team.all_players = $scope.team.players.concat($scope.team.ex_players);

        // sort by player code
        $scope.team.all_players.sort(function(a, b) {
            return parseInt(a.code) - parseInt(b.code);
        });
    };

    // call this function for the current month
    processExPlayers();

    console.log("$scope.scores.player_ids = " + $scope.scores.player_ids);
    $scope.playerHasScoreForMonth = function (player) {
//        console.log("playerHasScoreForMonth(): player.id = " + player.id + ", (" + typeof player.id + ")");
        // check for player id in the list of ids for the months scores
        return $scope.scores.player_ids.indexOf(player.id) != -1;
    };


    // TODO - function to grey-out the uncounted scores
    $timeout(function() {
        $("td:contains('*')").css("font-color", "#A9A9A9");
    }, 500);

    $scope.editTeamName = function () {
        var modalInstance = $modal.open({
          templateUrl: TEMPLATE_PATH + 'main-panel/teams/editTeamNameModal.html',
          controller: 'EditTeamNameController',
          scope: $scope,
        });
        modalInstance.result.then(function (update_team) {
            console.log('editTeamName: modalInstance response:' + JSON.stringify(update_team));

            Teams.patch(update_team).$promise
                .then(function (response) {
                    $scope.team.name = response.name;
//                    window.alert("Team name successfully changed.");
                },
                function(error) {
                    window.alert(JSON.stringify(error));
                });
        }, function () {
            console.info('editTeamName Modal dismissed at: ' + new Date());
        });
    };

    $scope.editTeamLineup = function () {
        // redirect to the line-up url
        console.log("editTeamLineup: " + $location.path() + '/lineup/');
        $location.path($location.path() + 'lineup/');
    };

}]);

footyApp.controller('EditTeamNameController', ['$scope', '$modalInstance', function($scope, $modalInstance) {

    $scope.update_team = {
        id: $scope.team.id,
        name: $scope.team.name
    };

    $scope.saveTeamName = function() {
        $modalInstance.close($scope.update_team);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);


footyApp.filter('trustAsHtml', function($sce) { return $sce.trustAsHtml; });

footyApp.controller('TeamLineupController', ['$scope', '$rootScope', '$route', 'Players', 'TeamValidate','teamDetails', 'currentWindow', function($scope, $rootScope, $route, Players, TeamValidate, teamDetails, currentWindow) {
    $scope.team = teamDetails;
    $scope.currentWindow = currentWindow;
    console.log("TeamLineupController: $scope.currentWindow = " + JSON.stringify($scope.currentWindow));

    // create a record of current statuses:
    var oldStatuses = {};
    angular.forEach($scope.team.players, function(player) {
        oldStatuses[player.id] = player.status;
    });

    $scope.team.players.GKP = {
        F: new Array(1),
        R: new Array(1)
    }
    $scope.team.players.DEF = {
        F: new Array(4),
        R: new Array(1)
    }
    $scope.team.players.MID = {
        F: new Array(4),
        R: new Array(1)
    }
    $scope.team.players.STR = {
        F: new Array(2),
        R: new Array(1)
    }
    $scope.team.players.SQUAD = [];

    // initialize the player position arrays with the existing line-up
    angular.forEach(teamDetails.players, function(player) {
        if (player.status == 'F' || player.status == 'R') {
            angular.forEach($scope.team.players[player.position][player.status], function(value) {
                if (value == undefined) {
                    value = player;
                }
            });
        } else {
            $scope.team.players.SQUAD.push(player);
        }

    });

    console.log("$scope.team: " + JSON.stringify($scope.team, null, 4));

    $scope.validateTeamSelection = function () {


    };

    $scope.saveTeam = function () {
        angular.forEach($scope.team.players, function(player) {
            if (oldStatuses[player.id] != player.status) {
            console.log("saveTeam(): changing " + player.name + " from " + oldStatuses[player.id] + " to " + player.status );
                Players.patch(player).$promise
                    .then(function (response) {
        //                window.alert(JSON.stringify(response));
                    },
                    function (error) {
                        window.alert(JSON.stringify(error));
                    });
            };
        });

        TeamValidate.get({id: $scope.team.id}).$promise
            .then(function (response) {
                console.log("saveTeam(): response = " + JSON.stringify(response));
                console.log("saveTeam(): typeof(response.is_valid) = " + typeof(response.is_valid));
                console.log("saveTeam(): response.is_valid = " + response.is_valid);
                if (response.is_valid) {
                    window.alert("A valid team line-up was saved successfully.");
                } else {
                    window.alert("WARNING - Team line-up is not valid!!");
                }

            });

        $route.reload();
    };

}]);

footyApp.controller('TeamLineupControllerNEW', ['$scope', '$rootScope', '$route', 'Players', 'TeamValidate','teamDetails', 'currentWindow', function($scope, $rootScope, $route, Players, TeamValidate, teamDetails, currentWindow) {
    $scope.team = teamDetails;
    $scope.currentWindow = currentWindow;
    console.log("TeamLineupController: $scope.currentWindow = " + JSON.stringify($scope.currentWindow));

    // create a lookup dict of current statuses key = player.id:
    var oldStatuses = {};
    angular.forEach($scope.team.players, function(player) {
        oldStatuses[player.id] = player.status;
    });

    function addTeamPositions(object) {
        // add arrays representing the team positions to an object
        object.GKP = {
            F: new Array(1).fill(),
            R: new Array(1).fill()
        }

        object.DEF = {
            F: new Array(4).fill(),
            R: new Array(1).fill()
        }

        object.MID = {
            F: new Array(4).fill(),
            R: new Array(1).fill()
        }

        object.STR = {
            F: new Array(2).fill(),
            R: new Array(1).fill()
        }

        object.SQUAD = [];
    }

    $scope.team.currentPositions = {};
    addTeamPositions($scope.team.currentPositions);

    $scope.team.newPositions = {};
    addTeamPositions($scope.team.newPositions);

//    $scope.team.currentPositions.GKP = {
//        F: new Array(1).fill(),
//        R: new Array(1).fill()
//    }
//    $scope.team.currentPositions.DEF = {
//        F: new Array(4).fill(),
//        R: new Array(1).fill()
//    }
//    $scope.team.currentPositions.MID = {
//        F: new Array(4).fill(),
//        R: new Array(1).fill()
//    }
//    $scope.team.currentPositions.STR = {
//        F: new Array(2).fill(),
//        R: new Array(1).fill()
//    }
//    $scope.team.currentPositions.SQUAD = [];

    console.log("")
    console.log("BEGIN")
    console.log("")

    var expectedPlayerCounts = [
        {position: 'GKP', status: 'F', count: 1},
        {position: 'GKP', status: 'R', count: 1},
        {position: 'DEF', status: 'F', count: 4},
        {position: 'DEF', status: 'R', count: 1},
        {position: 'MID', status: 'F', count: 4},
        {position: 'MID', status: 'R', count: 1},
        {position: 'STR', status: 'F', count: 2},
        {position: 'STR', status: 'R', count: 1},
    ]

    function countPlayers(position, status) {
        // returns a count of the players in a given position with a given status
        angular.forEach($scope.team.players, function(player) {
            var count = 0;
            if (player.position == position && player.status == status) {
                count += 1;
            }
        })

        return count;
    }

    // an array of error messages for validation
    $scope.validationErrors = [];

    function validateLineUp () {
        // count the players in each position & status and return a boolean indicating whether the line is valid
        // records errors messages in $scope.validationErrors

        // reset an errors first
        $scope.validationErrors = [];

        angular.forEach(expectedPlayerCounts, function(expected) {
            var count = countPlayers(expected.position, expected.status);
            if (expected.count != count) {
                $scope.validationErrors.push()
            }
        })

    }


    function populatePlayers(positions) {
        // initialize the player position arrays with currently selected line-up
        angular.forEach($scope.team.players, function(player) {
            if (player.status == 'F' || player.status == 'R') {
                angular.forEach(positions[player.position][player.status], function(value, index) {
                    if (value == undefined) {
                        positions[player.position][player.status][index] = player;
                    }
                });
            } else {
                positions.SQUAD.push(player);
            }
        });
    }

    populatePlayers($scope.team.currentPositions);


    console.log("$scope.team.currentPositions = " + JSON.stringify($scope.team.currentPositions));
    console.log("$scope.team.newPositions = " + JSON.stringify($scope.team.newPositions));

    console.log("")
    console.log("END")
    console.log("")

    function arrayIsFull(array) {
        return array.indexOf(undefined) == -1
    }

    function addPlayerToPosition(player) {
//        angular.forEach(teamDetails)
    }


    $scope.changesToSave = {};


    $scope.changePlayerStatus = function (player) {
        // the status has changed from the original, add it to the list to save
        if (oldStatuses[player.id] != player.status) {
            $scope.changesToSave[player.id] = player.status
        } else {
            delete $scope.changesToSave[player.id]
        }
    }

    $scope.validateTeamSelection = function () {


    };

    $scope.saveSquadChanges = function () {
        angular.forEach($scope.team.players, function(player) {
            if (oldStatuses[player.id] != player.status) {
            console.log("saveTeam(): changing " + player.name + " from " + oldStatuses[player.id] + " to " + player.status );
                Players.patch(player).$promise
                    .then(function (response) {
        //                window.alert(JSON.stringify(response));
                    },
                    function (error) {
                        window.alert(JSON.stringify(error));
                    });
            };
        });

        TeamValidate.get({id: $scope.team.id}).$promise
            .then(function (response) {
                console.log("saveTeam(): response = " + JSON.stringify(response));
                console.log("saveTeam(): typeof(response.is_valid) = " + typeof(response.is_valid));
                console.log("saveTeam(): response.is_valid = " + response.is_valid);
                if (response.is_valid) {
                    window.alert("A valid team line-up was saved successfully.");
                } else {
                    window.alert("WARNING - Team line-up is not valid!!");
                }

            });

        $route.reload();
    };

}]);


footyApp.controller('MotmController', ['$scope', '$location', '$rootScope', 'monthlyScores', function($scope, $location, $rootScope, monthlyScores) {
    $scope.monthlyScores = monthlyScores;

    // add a status for tracking open/closed stat of the accordion widget for each month...
    angular.forEach($scope.monthlyScores, function(score) {
        score.isOpen = false;
    });
    // ...and make the first one open by default
    $scope.monthlyScores[0].isOpen = true;


    $rootScope.baseUrl = $location.path();

}]);


footyApp.controller('ActivityStreamController', ['$scope', '$rootScope', '$route', '$interval', 'STATIC_ROOT', 'ActivityStreamData', 'ActivityComment', function($scope, $rootScope, $route, $interval, STATIC_ROOT, ActivityStreamData, ActivityComment) {
	var StreamData = new ActivityStreamData.Stream($route.current.params.space_id);
	$scope.stream = function() { return StreamData.getStream(); };
	$scope.loading_more = function() { return StreamData.loading(); };
	$scope.loadMore = function () { StreamData.loadMore(); };
	StreamData.startPolling();
	
	//var activitiesPoll = $interval(StreamData.pollForActivities, StreamData.poll_seconds);
 	//ActivityStreamData.init();

	var fileExt = /\.(\w{1,4})$/;

	$scope.iconFor = function(object) {
		var matches = fileExt.exec(object.name);
		return STATIC_ROOT + 'images/icons/' + matches[1].toLowerCase() + '-icon-64x64.png';
	};


	// Add comment callback
	$scope.addComment = function(activity, comment) {
		ActivityComment.post({activity: activity.id, text: comment}, function(data) {
			activity.comments.push(data);
		});
	};

	// Add status update callback
	$scope.updated = function(status) {
		$scope.stream.unshift(status);
	};

	$scope.selectSpace = function(space) {
		$rootScope.$emit('select_space', space);
	};

	$rootScope.$on('activity_stream_ready', function(event, data){
		$scope.stream = data;
	});

	// Tidy up when scope destroyed
	$scope.$on('$destroy', function() {
		StreamData.stopPolling();
	});

}]);

footyApp.factory('ActivityStreamData', ['$rootScope', '$q', '$interval', 'ActivityStream', 'ActivityComment', 'ServerTime', function($rootScope, $q, $interval, ActivityStream, ActivityComment, ServerTime) {

	// Normally Angular factories produce singletons but we need to maintain state across
	// shared instances so this factory instantiates a new class each time.

	// Constructor
	var StreamData = function(space) {
		//angular.extend(this, space);
		this.loading_more = true;
		this.stream = [];
		this.stream_page = 1;
		this.space = space;
		console.log('Stream for space ' + this.space);
		var self = this;
		var poll_seconds = $q.defer();
		this.poll_time_seconds = poll_seconds.promise;

		ActivityStream.query({space: this.space, page_size: 5}, function(data) {
			self.stream = data.results;
			//newActivity(self.stream);
			self.loading_more = data.next == null;
			// Sync time
			ServerTime.get({}, function(server_time) {
				poll_seconds.resolve(server_time.poll_time_seconds * 1000);
				var serverTime = moment(server_time.server_time);
				self.drift = moment.duration(moment() - serverTime); // Difference between browser and server times
				self.activitiesSince = self.now(); // Now
				self.commentsSince = self.activitiesSince.clone();
			});
		});
	};

	StreamData.prototype.loadMore = function () {
		// console.log("Loading more, page " + this.space);
		this.loading_more = true;
		var self = this;
		ActivityStream.query({space: this.space, page: ++this.stream_page},
			function(data) {
				if (data.next !== null) {
					self.loading_more = false;
				}
				for(var i=data.results.length-1; i>-1; i--) {
					self.stream.push(data.results[i]);
				}
				//newActivity(this.stream);
			}
			);
	};

	var now = function(drift) {
			return moment(moment() + drift);
	};

	StreamData.prototype.now = function() {
		return moment(moment() + this.drift);
	};

	StreamData.prototype.getStream = function () {
		//console.log('Getting stream');
		return this.stream;
	};

	StreamData.prototype.getPollSeconds = function () {
		return this.poll_seconds;
	};

	// Get new activities
	var pollForActivities = function(self) {
		//console.log("Polling for activities");
		ActivityStream.query({space: self.space, since: self.activitiesSince.toISOString()},
			function(data) {
				// console.log("Poll complete");
				self.activitiesSince = self.now();
				for(var i=data.results.length-1; i>-1; i--) {
					var has_activity = false;
					for (var j = 0; j < self.stream.length; j++) {
						if (self.stream[j].id == data.results[i].id) {
							has_activity = true;
							break;
						}
					};
					if (!has_activity) self.stream.unshift(data.results[i]);
				}
				//newActivity(this.stream);
			// }).$promise.finally(function() {
			// 	activitiesPoll = $timeout(pollForActivities, poll_seconds);
			});
	};

	// var activitiesPoll = $timeout(pollForActivities, poll_seconds);

	var pollForComments = function(self) {
		var promises = [];
		var spaces = [self.space];

		angular.forEach(spaces, function(space) {
			promises.push(ActivityComment.query({space: space, since: self.commentsSince.toISOString()}).$promise);
		});


		// Wait for all calls to complete and update comments
		$q.all(promises).then(function(all_comments) {
			self.commentsSince = self.now();
			angular.forEach(all_comments, function(comments) {
				angular.forEach(comments, function(comment) {
					for(var i=0; i<self.stream.length; i++) {
						if (self.stream[i].id == comment.activity) {
							var has_comment = false;
							angular.forEach(self.stream[i].comments, function(existing_comment) {
								if (existing_comment.id == comment.id) {
									has_comment = true;
									return;
								}
							});
							if (!has_comment) self.stream[i].comments.push(comment);
							break;
						}
					}
				});
			});
		// }).finally(function() {
		// 	commentsPoll = $timeout(pollForComments, poll_seconds);
		});
	};

	StreamData.prototype.startPolling = function() {
		var self = this;
		this.poll_time_seconds.then(function(poll_seconds) {
			// console.log("Polling every " + poll_seconds + " milliseconds");
			self.activitiesPoll = $interval(function() { pollForActivities(self); }, poll_seconds);
			self.commentsPoll = $interval(function() { pollForComments(self); }, poll_seconds);
		});
	};

	StreamData.prototype.stopPolling = function() {
		// console.log("Cancelling poll");
		if (angular.isDefined(this.activitiesPoll)) {
			$interval.cancel(this.activitiesPoll);
		}
		if (angular.isDefined(this.commentsPoll)) {
			$interval.cancel(this.commentsPoll);
		}
	};

	var newActivity = function(data) {
		$rootScope.$emit('activity_stream_ready', data);
	};

	StreamData.prototype.loading = function() {
		// console.log(this);
		return this.loading_more;
	};

	// Tidy up when scope destroyed
	// $scope.$on('$destroy', function() {
	// 	if (angular.isDefined(activitiesPoll)) {
	// 		$timeout.cancel(activitiesPoll);
	// 		activitiesPoll = undefined;
	// 	}
	// 	if (angular.isDefined(commentsPoll)) {
	// 		$timeout.cancel(commentsPoll);
	// 		commentsPoll = undefined;
	// 	}
	// });

	return {
			Stream: StreamData
	};
}]);

footyApp.directive('miniActivityStream', ['ActivityStreamData', 'TEMPLATE_PATH', 'STATIC_ROOT', '$rootScope', function(ActivityStreamData, TEMPLATE_PATH, STATIC_ROOT, $rootScope) {

	var link = function(scope, element, attrs) {
		var StreamData = new ActivityStreamData.Stream(0);
		scope.stream = function() { return StreamData.getStream(); };
		// scope.loading_more = StreamData.loading_more;
		// scope.loadMore = StreamData.loadMore;
		StreamData.startPolling();

		var fileExt = /\.(\w{1,4})$/;

		scope.iconFor = function(object) {
			var matches = fileExt.exec(object.name);
			return STATIC_ROOT + 'images/icons/' + matches[1].toLowerCase() + '-icon-16x16.png';
		};

		$rootScope.$on('activity_stream_ready', function(event, data){
			scope.stream = data;
		});
	};


	return {
		restrict: 'E',
		replace: true,
		templateUrl: TEMPLATE_PATH + 'main-panel/activity/activity-stream-mini.html',
		link: link
	};	
}]);

footyApp.directive('activityComment', ['$route', 'TEMPLATE_PATH', function($route, TEMPLATE_PATH) {
	return {
		restrict: 'E',
		replace: true,
		scope: {
			activity: '=',
			'addComment': '&onAddComment',
		},
		templateUrl: TEMPLATE_PATH + 'main-panel/activity/activity-comment.html',
		link: function(scope, element, attrs) {
			scope._addComment = function() {
				scope.addComment({activity: scope.activity, comment: scope.comment});
				scope.comment = undefined;
			};
		}
	};
}]);

footyApp.directive('activityStatus', ['$route', 'TEMPLATE_PATH', 'StatusUpdate', function($route, TEMPLATE_PATH, StatusUpdate) {
	return {
		restrict: 'E',
		replace: true,
		transclude: true,
		scope: {
			'updated': '&onUpdated',
		},
		templateUrl: TEMPLATE_PATH + 'main-panel/activity/activity-status.html',
		link: function(scope, element, attrs) {
			scope.updateStatus = function() {
				var status = {message: scope.message, content_model: '', space: $route.current.params.space_id};
				StatusUpdate.post(status, function(update) {
					scope.message = undefined;
					scope.updated({status: update});
				});
			};
		}
	};
}]);

footyApp.controller('DocumentsController', ['$scope', '$route', '$location', '$modal', 'files', 'paths', 'TEMPLATE_PATH', '$timeout', 'FileStorage', 'FileStoragePaths', 'session', function($scope, $route, $location, $modal, files, paths, TEMPLATE_PATH, $timeout, FileStorage, FileStoragePaths, session) {
	$scope.browser = {
		current_path: paths.current_path,
		path: paths.current_path.full_path,
		viewMode: session.viewmode || 'grid',
		setMode: function(mode) {
			$scope.browser.viewMode = session.viewmode = mode;
		},
		files: files,
		paths: paths.paths,
	};

	$scope.selectedObject = undefined;

	$scope.show_delete = function() {
		if ($scope.selectedObject) {
			if ($scope.selectedObject.content) {
				if ($scope.permissions.can_delete) return true;
			} else {
				if ($scope.permissions.can_delete_folder) return true;
			}
		}
		return false;
	};

	$scope.uploadFile = function (size) {
	    var modalInstance = $modal.open({
	      templateUrl: TEMPLATE_PATH + 'main-panel/fileUpload.html',
	      controller: 'FileUploadControl',
	      size: size,
	      resolve: {
		      path_id: function() { return $scope.browser.current_path.id; },
		      files: function() { return $scope.browser.files; },
	      }
    	});
	    modalInstance.result.then(function (result) {
	    	if (result.update) {
	    		for (var i=0; i<$scope.browser.files.length; i++) {
	    			if ($scope.browser.files[i].id === result.file.id) {
	    				$scope.browser.files[i] = result.file;
	    				break;
	    			}
	    		}
	    	} else {
	    		$scope.browser.files.push(result.file);
	    	}
    	}, function () {
      		//$log.info('Modal dismissed at: ' + new Date());
    	});
	};

	$scope.newFolder = function (size) {
	    var modalInstance = $modal.open({
	      templateUrl: 'newFolder.html',
	      controller: 'NewFolderControl',
	      size: size,
	      resolve: {
		      path_id: function() { return $scope.browser.current_path.id; },
		      space_id: function() { return $route.current.params.space_id; },
	      }
    	});
	    modalInstance.result.then(function (result) {
      		$scope.browser.paths.push(result);
    	}, function () {
      		//$log.info('Modal dismissed at: ' + new Date());
    	});
	};

	$scope.select = function(object) {
		if ($scope.selectedObject) $scope.selectedObject.$$select(false);
		object.$$select(true);
		$scope.selectedObject = object;
	};

	$scope.delete = function() {
		if ($scope.selectedObject.content) {
		    var modalInstance = $modal.open({
		      templateUrl: 'confirmModal.html',
		      controller: 'ConfirmOperationController',
		      size: 'm',
		      resolve: {
			      modal: function () { return {title: 'Please confirm', message: 'Are you sure you want to delete "<em>' + $scope.selectedObject.name + '</em>"?'}; },
		      }
	    	});
		    modalInstance.result.then(function (result) {
				FileStorage.remove({id: $scope.selectedObject.id}).$promise.then(
					function() {
						for (var i=0; i<$scope.browser.files.length; i++) {
							if ($scope.browser.files[i].id === $scope.selectedObject.id) {
								$scope.browser.files.splice(i, 1);
								break;
							}					
						}
						$scope.selectedObject = undefined;
					},
					function(response) {
					    var modalInstance = $modal.open({
					      templateUrl: 'errorModal.html',
					      controller: 'ModalErrorControl',
					      //size: 's',
					      resolve: {
					      	error: function() { return { title: 'Unable to delete', message: response.data.detail }; },
					      }
				    	});
					    modalInstance.result.then(function (result) {
				      		//object.name = object._name;
				    	}, function () {
				      		//$log.info('Modal dismissed at: ' + new Date());
				    	});
					}
					);
	    	}, function () {
	      		//$log.info('Modal dismissed at: ' + new Date());
	    	});

		} else {
		    var modalInstance = $modal.open({
		      templateUrl: 'confirmModal.html',
		      controller: 'ConfirmOperationController',
		      size: 'm',
		      resolve: {
			      modal: function () { return {title: 'Please confirm', message: '<p>Are you sure you want to delete "<em>' + $scope.selectedObject.name + '</em>"?</p><p class="text-danger"><strong>WARNING: This will delete all files and folders in this folder!</strong></p>'}; },
		      }
	    	});
		    modalInstance.result.then(function (result) {
				FileStoragePaths.remove({id: $scope.selectedObject.id}).$promise.then(
					function() {
						for (var i=0; i<$scope.browser.paths.length; i++) {
							if ($scope.browser.paths[i].id === $scope.selectedObject.id) {
								$scope.browser.paths.splice(i, 1);
								break;
							}					
						}
						$scope.selectedObject = undefined;
					},
					function(response) {
					    var modalInstance = $modal.open({
					      templateUrl: 'errorModal.html',
					      controller: 'ModalErrorControl',
					      //size: 's',
					      resolve: {
					      	error: function() { return { title: 'Unable to delete', message: response.data.detail }; },
					      }
				    	});
					    modalInstance.result.then(function (result) {
				      		//object.name = object._name;
				    	}, function () {
				      		//$log.info('Modal dismissed at: ' + new Date());
				    	});
					}
					);
	    	}, function () {
	      		//$log.info('Modal dismissed at: ' + new Date());
	    	});
		}
	};

	$scope.viewOrDownload = function(object) {
	    var modalInstance = $modal.open({
	      templateUrl: 'filePreview.html',
	      controller: 'ModalFilePreviewControl',
	      size: 'lg',
	      resolve: {
	      	file: function() { return object; },
	      }
    	});
	    // modalInstance.result.then(function (result) {
     //  		object.name = object._name;
    	// }, function () {
     //  		//$log.info('Modal dismissed at: ' + new Date());
    	// });

	};

	var changePath = function(path) {
		var space_id = $route.current.params.space_id;
		$location.path('/' + space_id + '/documents/!' + path.full_path);
	};

	$scope.changePath = changePath;

	$scope.refresh = function() {
		$route.reload();
	};

	$scope.parent = function() {
		var parent_path;
		angular.forEach($scope.browser.paths, function(value, key) {
			if (value.id == $scope.browser.current_path.parent) {
				parent_path = value;
				return;
			}
		});
		changePath(parent_path);
	};

	$scope.rename = function (object) {
		if (object.content) {
			// File
			FileStorage.rename({id: object.id, name: object._name}).$promise.then(
				function(data) {
					// Success
					for(var i=0; i<$scope.browser.files.length; i++) {
						if ($scope.browser.files[i].id === data.id) {
							$scope.browser.files[i] = data;
							break;
						}
					}
				},
				function(response) {
					//console.log(response);
				    var modalInstance = $modal.open({
				      templateUrl: 'errorModal.html',
				      controller: 'ModalErrorControl',
				      //size: 's',
				      resolve: {
				      	error: function() { return { title: 'Unable to rename', message: response.data.non_field_errors[0] }; },
				      }
			    	});
				    modalInstance.result.then(function (result) {
			      		//object.name = object._name;
			    	}, function () {
			      		//$log.info('Modal dismissed at: ' + new Date());
			    	});

				});
		} else {
			// Path
			FileStoragePaths.rename({id: object.id, name: object._name}).$promise.then(
				function(data) {
					// Success
					for(var i=0; i<$scope.browser.paths.length; i++) {
						if ($scope.browser.paths[i].id === data.id) {
							$scope.browser.paths[i] = data;
							break;
						}
					}
				},
				function(response) {
					//console.log(response);
				    var modalInstance = $modal.open({
				      templateUrl: 'errorModal.html',
				      controller: 'ModalErrorControl',
				      //size: 's',
				      resolve: {
				      	error: function() { return { title: 'Unable to rename', message: response.data.__all__[0] }; },
				      }
			    	});
				    modalInstance.result.then(function (result) {
			      		//object.name = object._name;
			    	}, function () {
			      		//$log.info('Modal dismissed at: ' + new Date());
			    	});
				});
		}
	};

}]);

footyApp.controller('ModalErrorControl', ['$scope', '$modalInstance', 'error', function($scope, $modalInstance, error) {
	$scope.error = error;
	$scope.ok = function() {
		$modalInstance.close();
	};
}]);

footyApp.controller('ModalFilePreviewControl', ['$scope', '$modalInstance', 'file', function($scope, $modalInstance, file) {
	$scope.file = file;
	$scope.ok = function() {
		$modalInstance.close();
	};
}]);

footyApp.controller('WikiPortalController', ['$scope', '$route', 'sections', function($scope, $route, sections) {
	$scope.params = $route.current.params;

	$scope.pages = ['Contents']; // , 'Portals', 'Categories'];
	//$scope.main_sections = ['Reference', 'Research', 'Help']
	$scope.main_sections = sections;
}]);

footyApp.controller('WikiCategoryController', ['$scope', '$route', '$filter', 'category', 'subcategories', function($scope, $route, $filter, category, subcategories) {
	$scope.params = $route.current.params;

	var subcategories_sorted = {};
	var index = '';
	// Sort subcategories and index them
	angular.forEach($filter('orderBy')(subcategories, 'name'), function(value, key) {
		var ch = value.name.substring(0, 1);
		if (ch != index) {
			index = ch;
		}
		if (!subcategories_sorted[index]) {
			subcategories_sorted[index] = [];
		}
		subcategories_sorted[index].push(value);
	});
	// Sort pages and index them
	var pages_sorted = {};
	angular.forEach($filter('orderBy')(category.pages, 'title'), function(value, key) {
		var ch = value.title.substring(0, 1);
		if (ch != index) {
			index = ch;
		}
		if (!pages_sorted[index]) {
			pages_sorted[index] = [];
		}
		pages_sorted[index].push(value);
	});
	$scope.context = {
		category: category,
		subcategories: subcategories_sorted,
		subcategories_length: subcategories.length,
		pages: pages_sorted,
		pages_length: category.pages.length,
	};
}]);

footyApp.controller('WikiController', ['$scope', '$route', function($scope, $route) {
	$scope.params = $route.current.params;
	$scope.pages = ['Contents']; // , 'Portals', 'Categories'];
	$scope.main_sections = ['Reference', 'Research', 'Help'];

}]);

footyApp.controller('WikiPageController', ['$scope', '$location', '$route', '$modal', 'wikipage', 'pages', 'files_list', 'upload_path', 'category', 'WikiPages', 'Slugify', 'TEMPLATE_PATH', 'session',
	function($scope, $location, $route, $modal, wikipage, pages, files_list, upload_path, category, WikiPages, Slugify, TEMPLATE_PATH, session) {
	$scope.$location = $location;
	$scope.mode = $route.current.params.mode ? $route.current.params.mode : 'view';
	if ($scope.mode === 'view') {
		$scope.wikipage = session.wikipage = wikipage;
	} else {
		$scope.wikipage = session.wikipage;
	}
	$scope.pages = pages;

	$scope.tinymceOptions = {
		plugins: 'advlist autolink link image lists charmap print preview',
		toolbar: ["newdocument | undo redo | cut copy paste | removeformat bold italic underline strikethrough removeformat subscript superscript alignjustify alignleft aligncenter alignright | bullist numlist outdent indent blockquote | link image"],
		image_list: files_list,
		height: 550,
	};

	// Validation
	$scope.word = /^\w+$/;

	setViewMode = function() {
		$location.path('/' + $route.current.params.space_id + '/wiki/Section!' + $route.current.params.portalSection + '/' + $route.current.params.portalCategory + '/' + $scope.wikipage.link + '/');
	};


	$scope.save = function() {
		if ($scope.wikipage.id) {
			// Update
			WikiPages.put($scope.wikipage, function(response) {
				setViewMode();
			});
		} else {
			// New page
			//$scope.wikipage.current_revision.categories = [category.id];
			console.log("NEW: $scope.wikipage: " + JSON.stringify($scope.wikipage));
			WikiPages.save($scope.wikipage, function(response) {
				delete session.wikipage;
				setViewMode();
			});
		}
	};

	$scope.cancelEdit = function () {
		delete session.wikipage;
		setViewMode();
	};

	$scope.uploadFile = function (size) {
	    var modalInstance = $modal.open({
	      templateUrl: TEMPLATE_PATH + 'main-panel/fileUpload.html',
	      controller: 'FileUploadControl',
	      size: size,
	      resolve: {
		      path_id: function() { return upload_path.id; },
		      files: function() { return files_list; },
	      }
    	});
	    modalInstance.result.then(function (result) {
	    	var newFile = {title: result.file.name, value: result.file.content.url};
      		files_list.push(newFile);
    	}, function () {
      		//$log.info('Modal dismissed at: ' + new Date());
    	});
	};

	$scope.delete = function(size) {
		    var modalInstance = $modal.open({
		      templateUrl: 'confirmModal.html',
		      controller: 'ConfirmOperationController',
		      size: 'm',
		      resolve: {
			      modal: function () { return {title: 'Please confirm', message: 'Are you sure you want to delete "<em>' + $scope.wikipage.title + '</em>"?'}; },
		      }
	    	});
		    modalInstance.result.then(function (result) {
				WikiPages.remove({id: $scope.wikipage.id}).$promise.then(
					function() {
						$scope.wikipage = undefined;
					},
					function(response) {
					    var modalInstance = $modal.open({
					      templateUrl: 'errorModal.html',
					      controller: 'ModalErrorControl',
					      //size: 's',
					      resolve: {
					      	error: function() { return { title: 'Unable to delete', message: response.data.detail }; },
					      }
				    	});
					    modalInstance.result.then(function (result) {
				      		//object.name = object._name;
				    	}, function () {
				      		//$log.info('Modal dismissed at: ' + new Date());
				    	});
					}
					);
	    	}, function () {
	      		//$log.info('Modal dismissed at: ' + new Date());
	    	});
	};

}]);

footyApp.controller('NewPageModalControl', ['$scope', '$modalInstance', 'Slugify', 'categories', function($scope, $modalInstance, Slugify, categories) {
	console.log(categories);
	$scope.page = {
		title: '',
		categories: categories,
		category: '',
	};
	$scope.word = /^[\w\s()-]+$/;

	$scope.ok = function () {
    	var response = Slugify.post({title: $scope.page.title},
    		function() {
    			$scope.page.link = response.link;
      			$modalInstance.close($scope.page);
    		},
			function (response) {
				$scope.error_message = response.data.error_message;
			}
		);
  	};

  	$scope.cancel = function () {
    	$modalInstance.dismiss('cancel');
  	};
}]);


footyApp.factory('managers', ['$route', 'Managers', function($route, Spaces) {
                return {
                	data: function() {
                		var spaces = Managers.query(
                			function() {
                				spaces.push({
                					id: 0,
                					name: 'Personal',
                                    type: 'Personal'
                				});
                			}
                			);
                		return spaces.$promise;
                	}
                };
           }
]);

footyApp.factory('pluggable_apps', ['PluggableApps', '$timeout', '$route', '$q', function(PluggableApps, $timeout, $route, $q) {
                return {
                	apps: function() {
                		return PluggableApps.query().$promise;
                	}
                };
            }
]);

footyApp.directive('wikiNav', ['$route', '$location', '$filter', 'TEMPLATE_PATH', function($route, $location, $filter, TEMPLATE_PATH) {
	return {
		restrict: 'E',
		templateUrl: TEMPLATE_PATH + 'main-panel/wiki/wiki-nav.html',
		link: function(scope) {
			scope.selectPage = function(page) {
				//var routeparams = $route.current.params;
				$location.path('/' + $route.current.params.space_id + '/wiki/Portal!' + page);
			};
			scope.selectSection = function(section) {
				var routeparams = $route.current.params;
				$location.path('/' + $route.current.params.space_id + '/wiki/Portal!' + routeparams.portalPage + '/' + section);
			};
			scope.selectCategory = function(section, category) {
				$location.path('/' + $route.current.params.space_id + '/wiki/Section!' + section + '/' + category);
			};
			scope.categoriesFor = function(section) {
				var categories = $filter('filter')(scope.main_sections, {'name': section});
				if (categories.length > 0) {
					return categories[0].categories;
				} else {
					return [];
				}
			};
		}
	};
}]);

footyApp.directive('wikiNavbar', ['$route', '$location', '$filter', '$modal', 'TEMPLATE_PATH', 'WikiCategories', 'WikiPages', 'userHelperFactory', 'session', function($route, $location, $filter, $modal, TEMPLATE_PATH, WikiCategories, WikiPages, userHelperFactory, session) {
	return {
		restrict: 'E',
		transclude: true,
		templateUrl: TEMPLATE_PATH + 'main-panel/wiki/navbar.html',
		link: function(scope, element, attrs) {
			scope.open = function (size) {
			    var modalInstance = $modal.open({
			      templateUrl: 'newPageModal.html',
			      controller: 'NewPageModalControl',
			      size: size,
			      resolve: {
			        categories: function () {
			            return WikiCategories.query({space: $route.current.params.space_id}).$promise;
			        }
			      }
		    	});
			    modalInstance.result.then(function (page) {
			    	session.wikipage = page;
		      		$location.path('/' + $route.current.params.space_id + '/wiki/Section!' + $route.current.params.portalSection + '/' + page.category.name + "/" + page.link + '/edit/');
		    	}, function () {
		      		//$log.info('Modal dismissed at: ' + new Date());
		    	});
			};
			scope.editURL = function() {
				return '/' + $route.current.params.space_id + '/wiki/Section!' + $route.current.params.portalSection + '/' + $route.current.params.portalCategory + "/" + scope.wikipage.link + '/edit/';
			};

			scope.searcher = {
				search: function(isvalid) {
					if (isvalid) {
						var response = WikiPages.query({search: scope.searcher.search_text},
							function() {
								if (response.length>0) {
									scope.searcher.results = response;
									scope.searcher.isopen = true;
								}
							}
						);
					} else {
						scope.searcher.isopen = false;
					}
				},
				search_text: '',
				isopen: false,
				results: [],
			};

			userHelperFactory.then(function(user_detail) {
				scope.permissions = {
					can_add: user_detail.hasPermission($route.current.params.space_id, 'wiki', 'wikipage', 'C'),
					can_edit: user_detail.hasPermission($route.current.params.space_id, 'wiki', 'wikipage', 'M'),
					can_delete: user_detail.hasPermission($route.current.params.space_id, 'wiki', 'wikipage', 'D'),		
				};				
			});

			scope.breadcrumbs = function() {
				return session.breadcrumbs;
			};

		}
	};
}]);

footyApp.directive('storagePanel', ['$route', '$location', '$filter', '$modal', 'TEMPLATE_PATH', 'userHelperFactory', 'FileStorage', function($route, $location, $filter, $modal, TEMPLATE_PATH, userHelperFactory, FileStorage) {
	return {
		restrict: 'E',
		templateUrl: TEMPLATE_PATH + 'main-panel/documents/navbar.html',
		// transclude: true,
		// scope: {},
		link: function(scope, element, attrs) {

			// var changePath = function(path) {
			// 	console.log(path);
			// 	var space_id = $route.current.params.space_id;
			// 	$location.path('/' + space_id + '/documents/!' + path.full_path);
			// };

			// scope.changePath = changePath;

			// scope.refresh = function() {
			// 	$route.reload();
			// };

			// scope.parent = function() {
			// 	var parent_path;
			// 	angular.forEach(scope.browser.paths, function(value, key) {
			// 		if (value.id == scope.browser.current_path.parent) {
			// 			parent_path = value;
			// 			return;
			// 		}
			// 	});
			// 	changePath(parent_path);
			// };

			scope.searcher = {
				search: function(isvalid) {
					if (isvalid) {
						var response = FileStorage.query({space: $route.current.params.space_id, search: scope.searcher.search_text},
							function() {
								if (response.length>0) {
									scope.searcher.results = response;
									scope.searcher.isopen = true;
								}
							}
						);
					} else {
						scope.searcher.isopen = false;
					}
				},
				search_text: '',
				isopen: false,
				results: [],
			};

			// scope.select = function(obj) {
			// 	console.log('Click ' + obj.name);
			// };

			userHelperFactory.then(function(user_detail) {
				scope.permissions = {
					can_add: user_detail.hasPermission($route.current.params.space_id, 'storage', 'databasefile', 'C'),
					can_delete: user_detail.hasPermission($route.current.params.space_id, 'storage', 'databasefile', 'D'),		
					can_add_folder: user_detail.hasPermission($route.current.params.space_id, 'storage', 'databasefilepath', 'C'),
					can_delete_folder: user_detail.hasPermission($route.current.params.space_id, 'storage', 'databasefilepath', 'D'),
				};
			});
			

		}
	};
}]);

footyApp.directive('storageObject', ['$timeout', 'TEMPLATE_PATH', 'STATIC_ROOT', function($timeout, TEMPLATE_PATH, STATIC_ROOT) {
	return {
		restrict: 'E',
		transclude: true,
		scope: {
			'fnclick': '&onClick',
			'dblclick': '&onDblclick',
			'rename': '&onRename',
			'object': '=',
			'viewmode': '=',
		},
		templateUrl: TEMPLATE_PATH + 'main-panel/documents/storage-object.html',
		link: function(scope, element, attrs) {
			var singleClicked = false;
			var singleClickTimer;
			var clickCount = 0;
			var inputSelector = 'input#storage-object-' + scope.object.id;
			scope.renaming = false;
			scope.object.$$select = select;
			scope.newname = {name: ''};

			if (scope.object.content) {
				scope.class = 'glyphicon-file';
			} else {
				scope.class = 'glyphicon-folder-close';
			}

			var fileExt = /\.(\w{1,4})$/;

			scope.iconFor = function(object) {
				var matches = fileExt.exec(object.name);
				var iconSize = scope.viewmode == 'grid' ? '-icon-64x64.png' : '-icon-24x24.png';
				return STATIC_ROOT + 'images/icons/' + matches[1].toLowerCase() + iconSize;
			};


			scope.blur = function () {
				// Ignore blur if already hidden e.g. via 'Enter' key event
				if ($(inputSelector + ':visible').length) {
				    scope.renaming = false;
				    if (scope.object.name != scope.newname.name && scope.newname.name != '') {
						scope.object._name = scope.newname.name;
						//scope.object.name = scope.name;
						$timeout(scope.rename);
					}
				}
			};

			scope.keypress = function (event) {
				if (event.which === 27) {
					scope.renaming = false;
					scope.name = scope.object.name;
				}
				if (event.which === 13)
				{
					scope.blur();
				}
			};

			function select(selected) {
				var divElement = $(element.children()[0]);
				if (selected) {
					divElement.css({border: '1px solid'});
				}
				else {
					divElement.css({border: ''});
				}
			}

			function singleClick(event) {
				// Always fire single click event
				$timeout(scope.fnclick);
				clickCount = 0;
				if (singleClicked) {
					// Slow double-click
					singleClicked = false;
					scope.renaming = true;
					scope.newname.name = scope.object.name; // Shadow model
					$timeout(function() {
						select(false);
						$(inputSelector).focus();
					});
				} else {
					singleClicked = true;
					$timeout(function() {
						singleClicked = false;
					}, 1500);
				}
			}

			function doubleClick(event) {
				event.preventDefault();
				event.stopImmediatePropagation();
				$timeout.cancel(singleClickTimer);
				clickCount = 0;
				singleClicked = false;
				$timeout(scope.dblclick);
			}

			function delayClick(event) {
				var cloneEvent = $.Event('click', event);
				cloneEvent._delayedSingleClick = true;
				event.preventDefault();
				event.stopImmediatePropagation();
				singleClickTimer = $timeout(singleClick.bind(null, cloneEvent), 300);
			}

			element.on('click', function(event) {
				if (event._delayedSingleClick || scope.renaming) return;
				if (clickCount++) {
					doubleClick(event);
				} else {
					delayClick(event);
				}
			});
		},
	};
}]);

footyApp.directive('wikiLink', ['$route', function($route) {
	return {
		restrict: 'E',
		scope: {
			page: '=',
		},
		replace: true,
		template: '<a href="{{ href }}">{{ page.title }}</a>',
		link: function(scope, element, attrs) {
			scope.href = '/#' + (scope.page ? scope.page.full_link : '');
		}
	};
}]);

footyApp.directive('wikiCategoryLink', ['$route', function($route) {
	return {
		restrict: 'E',
		scope: {
			section: '=',
			category: '=',
		},
		replace: true,
		template: '<a href="{{ href }}">{{ category.name }}</a>',
		link: function(scope, element, attrs) {
			scope.href = '/#/' + $route.current.params.space_id + '/wiki/Section!' + scope.section.name + '/' + scope.category.name + '/';
		}
	};
}]);

footyApp.directive('fileLink', ['$route', function($route) {
	return {
		restrict: 'E',
		scope: {
			file: '=',
		},
		replace: true,
		template: '<a href="{{ href }}">{{ file.name }}</a>',
		link: function(scope, element, attrs) {
			scope.href = '/#/' + $route.current.params.space_id + '/documents/!' + scope.file.path.full_path;
		}
	};
}]);

footyApp.controller('FileUploadControl', ['$scope', '$modalInstance', 'FileUpload', 'path_id', 'files', function($scope, $modalInstance, FileUpload, path_id, files) {
	$scope.upload = {
		myFile: undefined,
	};

	var overwriting = false;
	var existing = undefined;

	$scope.ok = function () {

		if (!existing) {
			for(var i=0; i<files.length; i++) {
				if (files[i].name === $scope.upload.myFile.name) {
					$scope.error_message = 'A file with that name already exists. Press OK to overwrite.';
					existing = files[i];
					return;
				}
			}
			overwriting = true;
		} else {
			overwriting = true;
		}

		if (overwriting) {
			var id = existing ? existing.id : undefined;
	    	var promise = FileUpload.storeFile(id, $scope.upload.myFile, path_id);
	    	promise.then(
	        	function(response){
		      		$modalInstance.close({update: id !== undefined, file: response});
	        	},
	        	function(response){
	        		$scope.error_message = response.data.detail;
	        	}
			);
    	}
  	};

  	$scope.cancel = function () {
    	$modalInstance.dismiss('cancel');
  	};
}]);

footyApp.controller('NewFolderControl', ['$scope', '$modalInstance', 'FileStoragePaths', 'path_id', 'space_id', function($scope, $modalInstance, FileStoragePaths, path_id, space_id) {
	$scope.folder = {
		name: undefined,
	};

	$scope.validPath = /^[a-z0-9\s\(\)+=\[\]{}~;!\"\'£\$%&@]+$/i;

	$scope.ok = function () {

    	var promise = FileStoragePaths.post({name: $scope.folder.name, parent: path_id, space: space_id}).$promise;
    	promise.then(
        	function(response){
	      		$modalInstance.close(response);
        	},
        	function(response){
        		console.log('Fail');
        		console.log(response);
        		$scope.error_message = response.data.__all__[0];
        	}
		);
  	};

  	$scope.cancel = function () {
    	$modalInstance.dismiss('cancel');
  	};
}]);

footyApp.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;
            
            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);

footyApp.service('FileUpload', ['$http', 'FileStorage', function($http, FileStorage) {
    this.storeFile = function(id, file, path_id) {
        var fd = new FormData();
        fd.append('content', file);
        fd.append('path', path_id);
        if (id) fd.append('id', id);
        return FileStorage.post(fd).$promise;
    };
}]);

// User class

footyApp.factory('userHelperFactory', ['UserDetail', '$q', function(UserDetail, $q) {
	function UserHelper(user) {

		this.hasPermission = function(space, apptype, model, access_level, app_id) {
			app_id = typeof app_id !== 'undefined' ? app_id : null;
			for (var i=0; i<user.permissions.length; i++) {
				var p = user.permissions[i];
				if (p.apptype == apptype && p.model == model && p.access_level == access_level && p.app == app_id) {
					for (var s=0; s<p.spaces.length; s++) {
						if (space == p.spaces[s]) {
							return true;
						}
					}
					// Personal space
					if (space == 0 && p.spaces.length == 0) {
						return true;
					}
				}
			}

			return false;
		};
	}

	var deferred = $q.defer();

    var user = UserDetail.get(
        function() {
            deferred.resolve(new UserHelper(user));
    });

	return deferred.promise;
}]);

// Session class
// Holds state in the current browser window only and does not persist
footyApp.factory('session', [function() {
	return {'search': {},};
}]);

// directive for opening <a> links in a new window/tab
footyApp.directive('openInNewWindow', function() {
  return {
    compile: function(element) {
      var elems = (element.prop("tagName") === 'A') ? element : element.find('a');
      elems.attr("target", "_blank");
    }
  };
});

// unfinished code - abandoned in favour of the tab 'JSME EDITOR' approach - delete when that is fully implmented/tested
// footyApp.directive('structureSearch', ['$route', '$location', '$filter', '$modal', 'TEMPLATE_PATH', 'userHelperFactory', 'session', function($route, $location, $filter, $modal, TEMPLATE_PATH, userHelperFactory, session) {
	// return {
		// restrict: 'E',
		// transclude: true,
		// template: TEMPLATE_PATH + 'main-panel/tools/structure-search.html',
		// link: function(scope, element, attrs) {
			// scope.search = function (options) {
			    // var modalInstance = $modal.open({
			      // templateUrl: 'jsmeEditor.html',
			      // controller: 'StructureEditorCtrl',
			      // size: 'm',
			      // resolve: {
			        // // categories: function () {
			            // // return WikiCategories.query({space: $route.current.params.space_id}).$promise;
			        // // }
			        // options: options
			      // }
		    	// });
			    // modalInstance.result.then(function (smiles) {
			    	// session.wikipage = page;
		      		// $location.path('/' + $route.current.params.space_id + '/wiki/Section!' + $route.current.params.portalSection + '/' + page.category.name + "/" + page.link + '/edit/');
		    	// }, function () {
		      		// $log.info('StructureSearch Modal dismissed at: ' + new Date());
		    	// });
			// };
// 
			// // userHelperFactory.then(function(user_detail) {
				// // scope.permissions = {
					// // can_add: user_detail.hasPermission($route.current.params.space_id, 'wiki', 'wikipage', 'C'),
					// // can_edit: user_detail.hasPermission($route.current.params.space_id, 'wiki', 'wikipage', 'M'),
					// // can_delete: user_detail.hasPermission($route.current.params.space_id, 'wiki', 'wikipage', 'D'),		
				// // };				
			// // });
// 
			// scope.breadcrumbs = function() {
				// return session.breadcrumbs;
			// };
// 
		// }
	// };
// }]);
// 
// footyApp.controller('StructureEditorCtrl', ['$scope', '$modalInstance', 'Slugify', 'categories', function($scope, $modalInstance, Slugify, categories) {
	// console.log(categories);
	// $scope.page = {
		// title: '',
		// categories: categories,
		// category: '',
	// };
	// $scope.word = /^[\w\s()-]+$/;
// 
	// $scope.ok = function () {
    	// var response = Slugify.post({title: $scope.page.title},
    		// function() {
    			// $scope.page.link = response.link;
      			// $modalInstance.close($scope.page);
    		// },
			// function (response) {
				// $scope.error_message = response.data.error_message;
			// }
		// );
  	// };
// 
  	// $scope.cancel = function () {
    	// $modalInstance.dismiss('cancel');
  	// };
// }]);