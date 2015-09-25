(function () {
  'use strict';

  angular.module('cloudbrain.rtchart')
    .directive('rtChart', ['$matter', 'RtChart', function($matter, RtChart){

      var link = function(scope, element){
        scope.deviceNames = ['muse', 'OpenBCI'];

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
