(function () {
  'use strict';

  angular.module('cloudbrain.rtchart')
    .directive('rtChart', ['$rootScope', '$matter', 'RtChart', function($rootScope, $matter, RtChart){

      var link = function(scope, element){
        scope.deviceNames = ['muse', 'openbci'];

        scope.series = RtChart.getSeries();
        scope.data = RtChart.getData();
        scope.labels = RtChart.getLabels();
        scope.options = RtChart.chartConfig();

        scope.showChart = function () {
          RtChart.setDeviceType(scope.selectedDevice);
          RtChart.setDeviceId($matter.currentUser.username);
          RtChart.start(function(){
            scope.$apply();
          });
        };

        $rootScope.$watch('currentUser', function (newVal) {
          if(newVal == null) {
            RtChart.stop();
          }
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
