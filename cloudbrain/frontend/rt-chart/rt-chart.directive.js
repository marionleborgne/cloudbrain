(function () {
  'use strict';

  angular.module('cloudbrain.rtchart')
    .directive('rtChart', ['$rootScope', '$interval', '$matter', '$state', 'apiService', 'RtChart', function($rootScope, $interval, $matter, $state, apiService, RtChart){

      var link = function(scope, element){
        scope.deviceNames = ['muse', 'openbci'];
        scope.series = RtChart.getSeries();
        scope.data = RtChart.getData();
        scope.labels = RtChart.getLabels();
        scope.options = RtChart.chartConfig();
        scope.connected = false;

        if(!$rootScope.currentUser){
          $state.go('home');
        }

        scope.toggleConnection = function () {
          if(scope.connected === true){
            RtChart.stop();
          }else{
            RtChart.setDeviceType(scope.selectedDevice);
            RtChart.setDeviceId($rootScope.currentUser.username);
            RtChart.start();
            $interval(function () {}, 50);
          }
          scope.connected = !scope.connected;
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
