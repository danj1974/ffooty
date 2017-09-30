// angular.module('footyApp')

footyApp.filter('numberToFixedDp', function() {
	return function(value, decimalPlaces) {
        return  parseFloat(value).toFixed(decimalPlaces);
	};
});

footyApp.filter('objectByKeyValFilter', function () {
return function (input, filterKey, filterVal) {
    var filteredInput ={};
     angular.forEach(input, function(value, key){
       if(value[filterKey] && value[filterKey] !== filterVal){
          filteredInput[key]= value;
        }
     });
     return filteredInput;
}});

footyApp.filter('playerPosition', function () {
return function (players, position) {
    var filteredInput ={};
     angular.forEach(players, function(value, key){
       if (value.position == position){
          filteredInput[key]= value;
        }
     });
     return filteredInput;
}});