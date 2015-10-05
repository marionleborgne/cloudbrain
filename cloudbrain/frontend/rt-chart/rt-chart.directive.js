(function () {
  'use strict';

  angular.module('cloudbrain.rtchart')
    .directive('rtChart', ['$rootScope', '$interval', '$matter', 'apiService', 'RtChart', function($rootScope, $interval, $matter, apiService, RtChart){

      var link = function(scope, element){
        scope.deviceNames = ['muse', 'openbci'];
        scope.series = RtChart.getSeries();
        scope.data = RtChart.getData();
        scope.labels = RtChart.getLabels();
        scope.options = RtChart.chartConfig();

        scope.showChart = function () {
          RtChart.setDeviceType(scope.selectedDevice);
          RtChart.setDeviceId($matter.currentUser.username);
          RtChart.start();
          $interval(function () {}, 50);
        };

        $rootScope.$watch('currentUser', function (newVal) {
          if(newVal === null) {
            RtChart.stop();
          }
        });

        apiService.refreshPhysicalDeviceNames().then(function(response) {
          angular.copy(response.data, scope.deviceNames);
          console.log('devices loaded:', response);
        });

      };

      return {
        replace: true,
        restrict: 'E',
        scope: {

        },
        link: link,
        templateUrl: 'rt-chart/rt-chart-index.html'
      };

    }]);

})();
