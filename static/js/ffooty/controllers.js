footyApp.controller('BaseController', ['$scope', '$location', '$rootScope', 'UpdateScores', function($scope, $location, $rootScope, UpdateScores) {

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

    $rootScope.selectedPlayerIdsOld = [];

    function selectionChange() {
        $rootScope.selectedPlayers = $rootScope.gridOptions.selectedRows;
        $rootScope.selectedPlayerIds = [];

        angular.forEach($rootScope.gridOptions.selectedRows, function(value, key) {
            $rootScope.selectedPlayerIds.push(value.id);
        });

        setSelectionCounts();
        compareWithPreviousSelection();
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
        if ($rootScope.selectedPlayerIds.length > $scope.selectedPlayerIdsOld.length) {
            // a new row has been selected - do nothing
        } else {
            angular.forEach($scope.selectedPlayerIdsOld, function (id) {
                // find the player that has been unchecked
                if ($rootScope.selectedPlayerIds.indexOf(id) == -1) {
                    // check whether a nomination has been saved for the player...
                    var isNominated = false;
                    angular.forEach(userNoms, function(nomination) {
                        if (nomination.player == id) {
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
        suppressRowClickSelection: true,

    };

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
        $rootScope.selectedPlayers = $rootScope.gridOptions.selectedRows;
        $rootScope.selectedPlayerIds = [];

        angular.forEach($rootScope.gridOptions.selectedRows, function(value, key) {
            $rootScope.selectedPlayerIds.push(value.id);
        });

        setSelectionCounts();
        compareWithPreviousSelection();
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
        if ($rootScope.selectedPlayerIds.length > $scope.selectedPlayerIdsOld.length) {
            // a new row has been selected - do nothing
        } else {
            angular.forEach($scope.selectedPlayerIdsOld, function (id) {
                // find the player that has been unchecked
                if ($rootScope.selectedPlayerIds.indexOf(id) == -1) {
                    // check whether a nomination has been saved for the player...
                    var isNominated = false;
                    angular.forEach(userNoms, function(nomination) {
                        if (nomination.player == id) {
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
    };

    $scope.validateNominations();

    $scope.deleteNomination = function(player) {
        var index = $rootScope.selectedPlayers.indexOf(player)
        if (index != -1) {
            // remove from selectedPlayers & Ids arrays
            $rootScope.selectedPlayers.splice(index, 1);
            $rootScope.selectedPlayerIds.splice(index, 1);
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

footyApp.controller('AdminAuctionTeamsController', ['$scope', '$location', '$rootScope', '$filter', 'Players', 'teams', 'auctionTeamSummary', 'auctionRandomPlayerCodes', 'AuctionPassNominations', 'AuctionDealLogs', 'TEMPLATE_PATH', function($scope, $location, $rootScope, $filter, Players, teams, auctionTeamSummary, auctionRandomPlayerCodes, AuctionPassNominations, AuctionDealLogs, TEMPLATE_PATH) {

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
//            console.log("randomPlayerCodes = " + JSON.stringify($scope.randomPlayerCodes))

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

        if (p.team == undefined) {
            window.alert("Please set the Manager or click 'Pass / Cancel'");
        } else {

            Players.patch(p).$promise
                .then(function (response) {
                    $scope.auctionTeamSummary[p.team].players[position].push(p.sale)
                    $scope.auctionTeamSummary[p.team].funds -= p.sale;
                    $scope.selectedPlayer = {};
                    $scope.refreshAuctionDealLogs();
                },
                function (error) {
                    window.alert(JSON.stringify(error));
                });
        }
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

    $scope.passNominations = function() {
        var p = $scope.selectedPlayer;
        console.log("passNominations: " + JSON.stringify(p, null, 4));

        if (p.admin_auction_nomination_managers.length > 0) {
            AuctionPassNominations.get({player_id: p.id}).$promise
                .then(function(response) {
                    console.log('AuctionPassNominations: response = ' + JSON.stringify(response));
                    $scope.selectedPlayer = {};
                    $scope.refreshAuctionDealLogs();
                },
                function (error) {
                    window.alert(JSON.stringify(error));
                });
        } else {
            console.log("passNominations: no auction nominations to pass.");
        }
    };

    $scope.refreshAuctionDealLogs = function() {
        AuctionDealLogs.get().$promise
            .then(function(response) {
//                console.log('AuctionDealLogs: response = ' + JSON.stringify(response));
                $scope.auctionDealLogs = response.deals;
            },
            function (error) {
                window.alert(JSON.stringify(error));
            });
    }

    $scope.refreshAuctionDealLogs();

}]);

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
    };

    function compareWithPreviousSelection() {
        if ($rootScope.selectedPlayerIds.length > $scope.selectedPlayerIdsOld.length) {
            // a new row has been selected - uncheck it if the player is already bought
        } else {
            angular.forEach($scope.selectedPlayerIdsOld, function(id) {
                // find the player that has been unchecked
                if ($rootScope.selectedPlayerIds.indexOf(id) == -1) {
                    // check whether a nomination has been saved for the player...
                    var isNominated = false;
                    angular.forEach(userTransferNoms, function(nomination) {
                        if (nomination.player == id) {
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

footyApp.controller('ModalErrorControl', ['$scope', '$modalInstance', 'error', function($scope, $modalInstance, error) {
	$scope.error = error;
	$scope.ok = function() {
		$modalInstance.close();
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
