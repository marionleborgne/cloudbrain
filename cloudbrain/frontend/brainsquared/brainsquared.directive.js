(function () {
  'use strict';

  angular.module('cloudbrain.brainsquared')
    .directive('brainsquared', ['$rootScope', '$interval', 'apiService', 'ChartData', 'ChartConfig', function($rootScope, $interval, apiService, ChartData, ChartConfig){

      var link = function(scope, element){

        scope.charts = {
          series: ChartData.getSeries(),
          labels: ChartData.getLabels(),
          options: ChartConfig,
          left: {
            raw: ChartData.getData('left', 'raw'),
            accuracy: {

            }
          },
          right: {
            raw: ChartData.getData('right', 'raw'),
            accuracy: {

            }
          }
        };

        scope.connected = false;

        if(!$rootScope.currentUser){
          $state.go('home');
        }

        scope.toggleConnection = function () {
          if(scope.connected === true){
            ChartData.stop();
          }else{
            apiService.startDemoPublish();
            ChartData.start();
            $interval(function () {}, 50);
          }
          scope.connected = !scope.connected;
        };
      };

      return {
        replace: true,
        restrict: 'E',
        scope: {},
        link: link,
        templateUrl: 'brainsquared/brainsquared-index.html'
      };

    }]);

})();
