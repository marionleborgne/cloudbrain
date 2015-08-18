(function () {
  'use strict';
  angular.module('cloudbrain').controller('chartController', [
    '$scope',
    '$http',
    '$interval',
    '$log',
    function ($scope, $http, $interval, $log) {
      

    $scope.changeColor = function () {
        var color_val = 'rgba(255, 255, 255, 0.8)'
        $scope.chartConfig.options.chart.backgroundColor = color_val;
        $scope.chartPolar.options.chart.backgroundColor = color_val;
        $scope.chartBar.options.chart.backgroundColor = color_val;
      }
      $scope.getDevices = (function () {
        var url = 'http://datastore.cloudbrain.rocks/devices?callback=JSON_CALLBACK';
        $http.jsonp(url).success(function (data, status, headers) {
          $scope.device_names = data.filter(function (name) {
            return name !== '';
          });
        }).error(function (data, status, headers) {
          $log.log('Failed to Get Devices')
        });
      });
      $scope.getDevices();
      
      
      $scope.setChannelSeries = (function(data){
        var keys = Object.keys(data[0]);
        var key_length = keys.length;
        var channel_numbers = [];
        for (var obj of keys){
          if (obj != 'timestamp'){
            channel_numbers.push(obj);
            //$log.log(channel_numbers);
          };
        };
        //$log.log(channel_numbers);
        for (var obj in channel_numbers){
          //$log.log('object' +obj);
          $scope.chartConfig.series.push({name: channel_numbers[obj], data: [], id: obj, marker: {
            enabled: false,
            symbol: 'circle'
          }});
          $scope.chartStock.series.push({name: channel_numbers[obj], data: [], id: obj});
          //$log.log($scope.chartConfig.series.length);
        };
      });




$scope.url = 'http://datastore.cloudbrain.rocks/data?device_name=openbci&metric=eeg&device_id=marion&callback=JSON_CALLBACK';
$scope.getData = function (device) {
  $scope.chartConfig.title.text = device.name + ' ' + device.id;
  $scope.chartPolar.title.text = device.name + ' ' + device.id;
  $scope.chartBar.title.text = device.name + ' ' + device.id;
  $scope.chartStock.title.text = device.name + ' ' + device.id;
  var metric = 'eeg';
  var cloudbrain = 'http://datastore.cloudbrain.rocks/data?device_name='+device.name+'&metric='+metric+'&device_id='+device.id+'&callback=JSON_CALLBACK';
        //initialize series data for charts
        $http.jsonp(cloudbrain)
        .then(function(response){
          $scope.data = response.data;
          $scope.setChannelSeries($scope.data);
        },
        function(response){
          $log.log('fail');
        });

        $interval(function () {
          $http.jsonp($scope.url)
          .then(function(response){
            $scope.data = response.data;
        //$log.log($scope.chartConfig.series[0]);
        for (var obj in $scope.data){
              //$log.log(obj);
              var count = 0;
              for (var prop in $scope.data[obj]){
                if (prop != 'timestamp'){
                  //$log.log("data." + prop + "= " + $scope.data[obj][prop]);
                  //$log.log(count);
                  $scope.chartConfig.series[count].data.push($scope.data[obj][prop]);
                  $scope.chartStock.series[count].data.push($scope.data[obj][prop]);
                  //$log.log($scope.chartConfig.series[count].id);
                  //$log.log($scope.chartConfig.series);
                  count++
              //$log.log($scope.chartConfig.series[0].data);
            };
          };
        };
      },
      function(response){
        $log.log('fail');
      });
        }, 100, 50);
      };

      $scope.chartConfig =
      {
        options: {
          chart: {
            type: 'spline',
            /*backgroundColor: 'rgba(255, 255, 255, 0.2)'*/
          }
        },
        title: {
          text: 'EEG',
          x: - 20 //center
        },
        subtitle: {
          text: 'Source: cloudbrain.rocks',
          x: - 20
        },
        xAxis: {
          categories: [
          'time'
          ]
        },
        yAxis: {
          title: {
            text: 'uV'
          },
          plotLines: [
          {
            value: 0,
            width: 1,
            color: '#808080'
          }
          ]
        },
        legend: {
          layout: 'vertical',
          align: 'right',
          verticalAlign: 'middle',
          borderWidth: 0
        },
        series: [
        
        ],
        useHighStocks: true
      };

      $scope.chartStock = {
        options: {
          chart: {
            zoomType: 'x',
            type: 'spline'
          },
          legend: {
            enabled: true
          },
          rangeSelector: {
            buttons: [{
              count: 50,
              type: 'millisecond',
              text: '5S'
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
            shared: true,
            pointFormat: '<span style="color:{series.color}">{series.name}: <b>${point.y:,.0f}</b><br/>'
          },
          legend: {
            align: 'right',
            verticalAlign: 'top',
            layout: 'vertical'
          }
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
          min: 0
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
            shared: true,
            pointFormat: '<span style="color:{series.color}">{series.name}: <b>${point.y:,.0f}</b><br/>'
          },
          legend: {
            align: 'right',
            verticalAlign: 'top',
            y: 70,
            layout: 'vertical'
          }
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
          min: 0
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
    ]);
}) ();
