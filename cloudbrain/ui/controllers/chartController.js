/* global angular */
(function () { 'use strict';

var baseURL = 'http://demo.apiserver.cloudbrain.rocks';

angular.module('cloudbrain')

.controller('chartController',
           ['$scope','$http','$interval','$log','apiService','dataService',
function   ( $scope , $http , $interval , $log , apiService , dataService ) {

    $scope.model = {
      device: {
        id: undefined,
        name: undefined,
      },
      deviceIds: [],
      deviceNames: [],
      connected: false,
    };


    // apiService.refreshDeviceIds().then(function(response) {
    //   angular.copy(response.data, $scope.model.deviceIds);
    // });
    $scope.model.deviceIds = [ 'Demo' ];
    $scope.model.device.id = $scope.model.deviceIds[0];

    // apiService.refreshPhysicalDeviceNames().then(function(response) {
    //   angular.copy(response.data, $scope.model.deviceNames);
    // });
    $scope.model.deviceNames = [ 'muse', 'openbci' ];
    $scope.model.device.name = $scope.model.deviceNames[0];

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
              $scope[graphName].series[0].data.push(data[0].alpha);
          }
      }

      //$scope.url = 'http://mock.cloudbrain.rocks/data?device_name=openbci&metric=eeg&device_id=marion&callback=JSON_CALLBACK';
      $scope.showClick = false;
      $scope.chartMuse = false;
      $scope.button = 'Connect';
      $scope.disableButton = function () {
        if ($scope.deviceIdForm.$invalid || $scope.deviceIdForm.$pristine) {
            return true;
        } else if ($scope.deviceIdForm.$valid && $scope.deviceIdForm.$dirty) {
            $scope.button = 'Connect';
            return false
        } else {
          $scope.button = 'Connected';
          return false
        }
      }

      $scope.getData = function (device, url) {

        //Button UI Logic
        $scope.deviceIdForm.$setPristine();
        $scope.button = 'Connected';


        dataService.startPowerBand(device.name, device.id, function(data) {
          updatePowerBandGraph('chartPolar', data);
          updatePowerBandGraph('chartBar', data);
        });

        $scope.chartPolar.title.text = device.name + ' ' + device.id;
        $scope.chartBar.title.text = device.name + ' ' + device.id;
        $scope.chartStock.title.text = device.name + ' ' + device.id;
        $scope.showClick=true;
        if ('muse' === device.name){
          $scope.chartMuse = true;
        }
        var metric = 'eeg';
        $scope.lastTimestamp = Date.now() * 1000; //microseconds
        $scope.cloudbrain = baseURL + '/data?device_name='+device.name+'&metric='+metric+'&device_id='+device.id+'&callback=JSON_CALLBACK&start='+$scope.lastTimestamp;
        $scope.chart3 = $scope.chartStock.getHighcharts();

        //initialize series data for charts
        $http.jsonp($scope.cloudbrain)
          .then(function(response){
            setChannelSeries(response.data);
          }, function(response){
            $log.log('fail');
        });

        $interval(function () {
          $http.jsonp($scope.cloudbrain)
          .then(function(response){
            $scope.lastTimestamp = response.data[response.data.length - 1].timestamp;

            response.data.forEach(function (dataPoints) {
              delete dataPoints.timestamp;

              for(var channel in dataPoints){
                $scope.chartStock.series[channel.split('_')[1]].data.push(dataPoints[channel]);
                if($scope.chartStock.series[channel.split('_')[1]].data.length > 300){
                  $scope.chartStock.series[channel.split('_')[1]].data.shift();
                }
              }

            });

          },
          function(response){
            $log.log('fail');
          });
        }, 500);
      };



      $scope.chartStock = {
        options: {
          chart: {
            zoomType: 'x',
            type: 'spline'
          },
          tooltip: {
            enabled: false
          },
          legend: {
            enabled: true
          },
          rangeSelector: {
            buttons: [{
              count: 100,
              type: 'millisecond',
              text: '2S'
            }, {
              count: 300,
              type: 'millisecond',
              text: '30S'
            }, {
              type: 'all',
              text: 'All'
            }],
            selected: 0,
            inputEnabled: false
          },

          navigator: {
            enabled: true
          }
        },
        series: [],
        title: {
          text: 'EEG'
        },
        useHighStocks: true
      };

      $scope.chartPolar = {
        options: {
          chart: {
            polar: true,
            type: 'spline',
            margin: [
            50,
            50,
            50,
            50
            ]
          },
          pane: {
            size: '80%'
          },
          tooltip: {
            enabled: false,
            shared: true,
            pointFormat: '<span style="color:{series.color}">{series.name}: <b>${point.y:,.0f}</b><br/>'
          },
        },
        title: {
          text: 'EEG',
          x: - 80
        },
        xAxis: {
          categories: [
          'Gamma',
          'Delta',
          'Theta',
          'Beta',
          'Alpha'
          ],
          tickmarkPlacement: 'on',
          lineWidth: 0
        },
        yAxis: {
          gridLineInterpolation: 'polygon',
          lineWidth: 0,
          min: 0,
          max: 10,
        },
        series: [
        {
          name: 'Device 1',
          data: [
          43000,
          19000,
          60000,
          35000,
          17000
          ],
          pointPlacement: 'on',
          marker: {
            enabled: false,
            symbol: 'circle'
          }
        }
        ]
      };
      $scope.chartBar = {
        options: {
          chart: {
            margin: [
            50,
            50,
            50,
            50
            ],
            type: 'column'
          },
          pane: {
            size: '80%'
          },
          tooltip: {
            enabled: false,
            shared: true,
            pointFormat: '<span style="color:{series.color}">{series.name}: <b>${point.y:,.0f}</b><br/>'
          },
        },
        title: {
          text: 'EEG',
          x: - 80
        },
        xAxis: {
          categories: [
          'Gamma',
          'Delta',
          'Theta',
          'Beta',
          'Alpha'
          ],
          tickmarkPlacement: 'on',
          lineWidth: 0
        },
        yAxis: {
          gridLineInterpolation: 'polygon',
          lineWidth: 0,
          min: 0,
          max: 10,
        },
        series: [
        {
          name: 'Device 1',
          data: [
          43000,
          19000,
          60000,
          35000,
          17000
          ],
          pointPlacement: 'on',
          marker: {
            enabled: false,
            symbol: 'circle'
          }
        }
        ]
      };
    }
    ])

;

})();
