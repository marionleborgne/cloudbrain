/* global angular */
(function () {
  'use strict';

  angular.module('cloudbrain.home')

  .controller('HomeCtrl', ['$scope','$http','$interval','$log','apiService', 'API_URL', '$state',
  function ($scope , $http , $interval , $log , apiService , dataService, API_URL, $state) {

    $scope.model = {
      deviceIds: [],
      deviceNames: [],
    };

    $scope.changeColor = function () {
      var color_val = 'rgba(255, 255, 255, 0.8)';
      $scope.chartPolar.options.chart.backgroundColor = color_val;
      $scope.chartBar.options.chart.backgroundColor = color_val;
    };

    apiService.refreshPhysicalDeviceNames().then(function(response) {
      angular.copy(response.data, $scope.model.deviceNames);
      console.log('devices loaded:', response);
    });

    var setChannelSeries = function(data){
      var keys = Object.keys(data[0]);
      keys.forEach(function(key){
        if (key != 'timestamp'){
          for (var a=[],i=0;i<500;++i) a[i]=0;
          $scope.chartStock.series.push({name: key, data: a, id: key});
        }
      });
    };

    // FIXME: considering only the first point right now...
    function updatePowerBandGraph(graphName, data) {
      if (data.length) {
        $scope[graphName].series[0].data.length = 0;
        $scope[graphName].series[0].data.push(data[0].gamma);
        $scope[graphName].series[0].data.push(data[0].delta);
        $scope[graphName].series[0].data.push(data[0].theta);
        $scope[graphName].series[0].data.push(data[0].beta);
        $scope[graphName].series[0].data.push(data[0].alfa);
      }
    }

    //$scope.url = 'http://mock.cloudbrain.rocks/data?device_name=openbci&metric=eeg&device_id=marion&callback=JSON_CALLBACK';
    $scope.showClick = false;
    $scope.chartMuse = false;
    $scope.selectedDevice = '';
    $scope.getData = function (device, url) {
      $state.go('rtchart', {device:$scope.selectedDevice});
    }
  }
  ]);

})();
