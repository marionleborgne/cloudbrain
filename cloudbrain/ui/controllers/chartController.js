(function (){
	'use strict';

	angular.module('cloudbrain')

		.controller('chartController', ['$scope', '$http', '$interval', function($scope, $http, $interval){

           
            

			$scope.getData = function (device) {
				$scope.chartConfig.title.text = device.name + ' ' + device.id;
                if (device.name.toLowerCase() === 'openbci'){
                    $scope.num_channels = 8;
                } else if (device.name.toLowerCase() === 'muse'){
                    $scope.num_channels = 4;
                } else {
                    $scope.num_channels = 0;
                }


				var url = 'cloudbrain.rocks/api/' + device.name + '/' + device.id;
				$interval(function() {
                    $scope.cloudbrain_url='http://webserver.cloudbrain.rocks:6000/data?device_name=';
                    var end_of_string='&lt;muse/opnebci&gt;&metric=eeg&device_id=&lt;id&gt;';
                    $scope.url = "http://rest-service.guides.spring.io/greeting";
                    $http.get($scope.url)
                        .then(function(response){ //response if request succeeds
                            $scope.re = response;
                            console.log($scope.re);
                            
                        }, function(response){  //response if request failed

                        });
                    
                }, 100);

			};

		$scope.chartConfig =
		{
        options:{
            chart: {
                    type: "spline"
                    }
        },
        title: {
            text: 'EEG',
            x: -20 //center
        },
        subtitle: {
            text: 'Source: cloudbrain.rocks',
            x: -20
        },
        xAxis: {
            categories: ['time']
        },
        yAxis: {
            title: {
                text: 'uV'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: 'Tokyo',
            data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6],
            marker: {
                enabled: false,
                symbol: "circle"
                }
        }, {
            name: 'New York',
            data: [-0.2, 0.8, 5.7, 11.3, 17.0, 22.0, 24.8, 24.1, 20.1, 14.1, 8.6, 2.5],
            marker: {
                enabled: false,
                symbol: "circle"
                    }
        }, {
            name: 'Berlin',
            data: [-0.9, 0.6, 3.5, 8.4, 13.5, 17.0, 18.6, 17.9, 14.3, 9.0, 3.9, 1.0],
            marker: {
                enabled: false,
                symbol: "circle"
                }
        }, {
            name: 'London',
            data: [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8],
            marker: {
                enabled: false,
                symbol: "circle"
                    }
        }]
    };
        $scope.chartPolar = {
    options: {
            chart: {
                polar: true,
                type: 'spline'
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
          text: 'Budget vs spending ddd',
          x: -80
      },
      
      xAxis: {
          categories: ['Sales', 'Marketing', 'Development', 'Customer Support', 
                  'Information Technology', 'Administration'],
          tickmarkPlacement: 'on',
          lineWidth: 0
      },
          
      yAxis: {
          gridLineInterpolation: 'polygon',
          lineWidth: 0,
          min: 0
      },
      
      
      
      series: [{
          name: 'Allocated Budget',
          data: [43000, 19000, 60000, 35000, 17000, 10000],
          pointPlacement: 'on',
          marker: {
                enabled: false,
                symbol: "circle"
                }
      }]

  };

  $scope.barChart = {
    options: {
            chart: {
                
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
          text: 'Budget vs spending ddd',
          x: -80
      },
      
      xAxis: {
          categories: ['Sales', 'Marketing', 'Development', 'Customer Support', 
                  'Information Technology', 'Administration'],
          tickmarkPlacement: 'on',
          lineWidth: 0
      },
          
      yAxis: {
          gridLineInterpolation: 'polygon',
          lineWidth: 0,
          min: 0
      },
      
      
      
      series: [{
          name: 'Allocated Budget',
          data: [43000, 19000, 60000, 35000, 17000, 10000],
          pointPlacement: 'on',
          marker: {
                enabled: false,
                symbol: "circle"
                }
      }]

  };

		}]);



})();
