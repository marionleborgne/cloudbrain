/* global angular */
(function () { 'use strict';

  var app = angular.module('cloudbrain')
  app.controller('AppCtrl', ['$log','$rootScope', '$scope', '$matter', function ($log, $rootScope, $scope, $matter){
  	$scope.accountDropdownOptions = [{text:'Profile', click:'profile'},{text:'Logout', click:'logout()'}];
    $scope.isLoggedIn = function() {
      return $matter.isLoggedIn;
    };
    $scope.$watch('isLoggedIn()', function(newVal, oldVal){
      console.warn('logged in status changed', newVal, oldVal);
      if(!$scope.$$phase) {
        $scope.isLoggedIn = $matter.isLoggedIn;
        $rootScope.$digest();
      }
    });
    $scope.clickOption = function(ind){
  		var clickTask = $scope.accountDropdownOptions[ind];
  		$scope[clickTask];
  	};
  }]);
})();
