/* global angular */
(function () { 'use strict';

  var app = angular.module('cloudbrain', [
  	'ui.bootstrap',
  	'ui.router',
  	'ngMaterial',
  	'highcharts-ng',
    'cloudbrain.rtchart',
  	'cloudbrain.calibration',
  	'cloudbrain.account',
  	'cloudbrain.home'
  ]);
  app.config(function($mdThemingProvider) {
    $mdThemingProvider.definePalette('cloudbrain', {
      '50': 'ffebee',
      '100': 'ffcdd2',
      '200': 'ef9a9a',
      '300': 'ffffff',
      '400': 'ef5350',
      '500': 'f44336',
      '600': 'ffffff',
      '700': 'd32f2f',
      '800': 'c62828',
      '900': 'ffffff',
      'A100': '377BB5',
      'A200': '377BB5',
      'A400': '377BB5',
      'A700': '377BB5',
      'contrastDefaultColor': 'light',    // whether, by default, text (contrast)
                                        // on this palette should be dark or light
      'contrastDarkColors': ['50', '100', //hues which contrast should be 'dark' by default
       '200', '300', '400', 'A100'],
      'contrastLightColors': undefined    // could also specify this if default was 'dark'
    })

	  $mdThemingProvider.theme('default')
	    .primaryPalette('cloudbrain',  {
         'default': 'A200',
         'hue-1': '300',
         'hue-2': '600',
         'hue-3': '900'
       })
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
