(function (){
	'use strict';

	angular.module('cloudbrain')

		.controller('chartController', ['$scope', '$http', function($scope, $http){

			$scope.getData = function (device) {
				$scope.chartConfig.title.text = device.name + ' ' + device.id;

				// url = 'cloudbrain.rocks/api/' + device.name + '/' + device.id;
				// $interval(function () {
				// 	$http.get(url)
				// 		.success(function(response){
				//
				// 		})
				// 		.error(function(response){
				//
				// 		});
				// }, 100);

			}

			$scope.chartConfig =
					   {
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
        tooltip: {
            valueSuffix: '°C'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: 'Tokyo',
            data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
        }, {
            name: 'New York',
            data: [-0.2, 0.8, 5.7, 11.3, 17.0, 22.0, 24.8, 24.1, 20.1, 14.1, 8.6, 2.5]
        }, {
            name: 'Berlin',
            data: [-0.9, 0.6, 3.5, 8.4, 13.5, 17.0, 18.6, 17.9, 14.3, 9.0, 3.9, 1.0]
        }, {
            name: 'London',
            data: [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
        }]
    }
		}]);



})();
