(function () {
  'use strict';
  angular.module('cloudbrain').controller('chartController', [
    '$scope',
    '$http',
    '$interval',
    function ($scope, $http, $interval) {
      $scope.changeColor = function () {
        var color_val = 'rgba(255, 255, 255, 0.8)'
        $scope.chartConfig.options.chart.backgroundColor = color_val;
        $scope.chartPolar.options.chart.backgroundColor = color_val;
        $scope.chartBar.options.chart.backgroundColor = color_val;
      }
      $scope.getDevices = (function () {
        var url = 'http://datastore.cloudbrain.rocks/devices?callback=JSON_CALLBACK';
        $http.jsonp(url).success(function (data, status, headers) {
          //console.log(data);
          //console.log(status);
          //console.log('pass');
          $scope.device_names = data.filter(function (name) {
            return name !== '';
          });
          //console.log($scope.device_names);
        }).error(function (data, status, headers) {
          //console.log(data);
          //console.log(status);
          //console.log(headers);
        });
      });
      $scope.getDevices();
      
      $scope.url = 'http://datastore.cloudbrain.rocks/data?device_name=muse&metric=eeg&device_id=marion?callback=JSON_CALLBACK';
      
      $http({method: 'GET', url: $scope.url, responseType: "json"})
          .then(function(response){
            console.log(response);
            $scope.data = response.data;
          },
          function(response){
            console.log('fail');
            console.log(response.data);
          });


      $scope.getData = function (device) {
        $scope.chartConfig.title.text = device.name + ' ' + device.id;
        $scope.chartPolar.title.text = device.name + ' ' + device.id;
        $scope.chartBar.title.text = device.name + ' ' + device.id;
        if (device.name.toLowerCase() === 'openbci') {
          $scope.num_channels = 8;
        } else if (device.name.toLowerCase() === 'muse') {
          $scope.num_channels = 4;
        } else {
          $scope.num_channels = 0;
        }

        $interval(function () {
          $http({
            method: 'GET',
            url: $scope.url,
            responseType: 'json'
          }).success(function (data, status, headers) {
            console.log(data);
            console.log(status);
            console.log('pass');
            $scope.data = data;
            console.log($scope.data);
          }).error(function (data, status, headers) {
            console.log(data);
            console.log(status);
            console.log(headers);
            console.log('fail')
          });
        }, 1000);
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
        {
          name: 'Channel 1',
          data: [
          7,
          6.9,
          9.5,
          14.5,
          18.2,
          21.5,
          25.2,
          26.5,
          23.3,
          18.3,
          13.9,
          9.6
          ],
          marker: {
            enabled: false,
            symbol: 'circle'
          }
        },
        {
          name: 'Channel 2',
          data: [
          - 0.2,
          0.8,
          5.7,
          11.3,
          17,
          22,
          24.8,
          24.1,
          20.1,
          14.1,
          8.6,
          2.5
          ],
          marker: {
            enabled: false,
            symbol: 'circle'
          }
        },
        {
          name: 'Channel 3',
          data: [
          - 0.9,
          0.6,
          3.5,
          8.4,
          13.5,
          17,
          18.6,
          17.9,
          14.3,
          9,
          3.9,
          1
          ],
          marker: {
            enabled: false,
            symbol: 'circle'
          }
        },
        {
          name: 'Channel 4',
          data: [
          3.9,
          4.2,
          5.7,
          8.5,
          11.9,
          15.2,
          17,
          16.6,
          14.2,
          10.3,
          6.6,
          4.8
          ],
          marker: {
            enabled: false,
            symbol: 'circle'
          }
        }
        ]
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
