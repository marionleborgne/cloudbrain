/* global angular */
(function () { 'use strict';

  var app = angular.module('cloudbrain', [
  	'ui.bootstrap',
  	'ui.router',
  	'ngMaterial',
  	'highcharts-ng',
  	'cloudbrain.rtchart',
  	'cloudbrain.account',
  	'cloudbrain.home'
  ]);
  app.config(function($mdThemingProvider) {
	  $mdThemingProvider.theme('default')
	    .primaryPalette('blue')
	    .accentPalette('pink')
	});
  app.service('$matter', ['$log', '$window',  '$rootScope', function ($log, $window, $rootScope){
    var matter = new $window.Matter('cloudbrain', {localServer:false});
  	$log.log('Matter created:', matter);
  	$rootScope.matter = matter;
  	$rootScope.currentUser = matter.currentUser;
  	return matter;
  }]);
})();
