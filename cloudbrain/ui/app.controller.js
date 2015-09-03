/* global angular */
(function () { 'use strict';

  var app = angular.module('cloudbrain')
  app.controller('AppCtrl', ['$scope', '$matter', function ($scope, $matter){
  	$scope.accountDropdownOptions = [{text:'Profile', click:'profile'},{text:'Logout', click:'logout()'}];
  	$scope.isLoggedIn = function(){
  		return $matter.isLoggedIn;
  	};
  	$scope.clickOption = function(ind){
  		var clickTask = $scope.accountDropdownOptions[ind];
  		$scope[clickTask];
  	};
  	$scope.logout = function(){
  		$matter.logout().then(function(){
  			$log.log('Logout successful');
  		});
  	}
  }]);
})();
