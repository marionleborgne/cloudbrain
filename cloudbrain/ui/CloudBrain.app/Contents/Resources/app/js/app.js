'use strict';


var _GREEN = '#5cb85c';
var _RED = '#d9534f';
var _ORANGE = 'orange';
var _BLUE = "#337ab7";
var _HIGH_ANOMALY_AMPLITUDE = 6;
var _MEDIUM_ANOMALY_AMPLITUDE = 3;
var _LOW_ANOMALY_AMPLITUDE = 2;



// Angular App
var app = angular.module('cloudbrain', ["ui.bootstrap", "highcharts-ng"]);


// Main Screen Controller
app.controller('mainScreenController', ['$scope', '$interval', function ($scope, $interval) {

  // TODO: change that. hack to for the scope to refresh
  $interval(function () {}, 500);

  /*-------------*

    PYTHON

  *--------------*/

  
    var path = require('path');

    // call python
    var cmd = path.join(__dirname, 'python', 'dist', 'mock_connector', 'mock_connector');
    var child = require('child_process').execFile(cmd, [""], function(err, stdout,stderr){
    });

    console.log('Executed cmd: ' + cmd);


    // use event hooks to provide a callback to execute when data are available: 
    child.stdout.on('data', function(data) {
      var record = JSON.parse(data);
      $scope.chartSeries['metricValue'].data.shift();
      $scope.chartSeries['metricValue'].data.push(record['channel_0']['eeg']['value']);


    });


	


	/*-------------*

	  FILES

	*--------------*/


	$scope.files = [
		{
			name: 'Headset 1',
			metrics: {0: 'Channel 1', 1:'Channel 2', 2:'Channel 3'}
		},
		{
			name: 'Headset 2',
			metrics: {3:'Channel 1', 4:'Channel 2', 5:'Channel 3'}
		},
		{
			name: 'Headset 3',
			metrics: {6:'Channel 1', 7:'Channel 2', 8:'Channel 3'}
		}
	];




	/*-------------*

	  SHOW CHARTS

	*--------------*/

	// keep track of the charts we're showing
	$scope.chartsToShow = {};

	/*
	Example of how chartsToShow will be populated. Keys are the metric ID from above ˆˆˆ

		$scope.chartsToShow = {

			0: {
				fileName: 'Headset 1',
				metricName: 'Channel 1'
			},
			1: {
				fileName: 'Headset 1',
				metricName: 'Channel 2'
			}
		};
	*/





	// add or remove chart from chartsToShow, depending of wether the chart is laready being displayed or not.
	$scope.updateChart = function(fileName, metricId, metricName){

		if (metricId in $scope.chartsToShow){
			// pop the key
			delete $scope.chartsToShow[metricId];
		} else {

			$scope.chartsToShow[metricId] = {fileName: fileName, metricName: metricName};
		}
	};




	/*-------------*

	  DRAW CHARTS

	*--------------*/


	$scope.chartSeries =  {
		'lowAnomaly': 
		{
			type: 'column',
			name:'Low Anomaly',
			color: _GREEN,
			data: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		},
		'mediumAnomaly': 
		{
			type: 'column',
			name:'Medium Anomaly',
			color: _ORANGE,
			data: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		},  
		'highAnomaly':               
		{
			type: 'column',
			name:'High Anomaly',
			color: _RED,
			data: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		},
		'metricValue': 
		{
			type: 'spline',
			name: 'Metric Value',
			data: [1,2,3,4,5,6,7,8,9,1,1,2,3,4,5,6,7,8,9,1],
			color: _BLUE
		}
	};




	$scope.chartConfig = function(fileName, metricName) {

		return {

			series: $scope.chartSeries,
			title: {
				text: null,
			},
			c_REDits: {
				enabled: false
			},
			loading: false,
			options:
			{
				c_REDits: false,
				title:{
					//text: null
				},
				tooltip:{
					enabled: false,
					animation: false
				},
				plotOptions: {
					series: {
						stacking: 'normal'
					}
				},
				yAxis:{
					lineWidth:0,
					gridLineWidth: 0,
					minorGridLineWidth: 0,
					max:15,
					min:0,
					labels:{
						enabled:false
					},
					title: ''
				},

				legend: {
					enabled: true,
				}
			}
		};

	};

	/*
	$interval(function () {

		//var x = (new Date()).getTime();
		var anomalyLikelihood = Math.random() * 10;
		var metricValue = Math.random() * 10 ;

		var highAnomalyValue = 0;
		var mediumAnomalyValue = 0;
		var lowAnomalyValue = 0;
		if (anomalyLikelihood >= 8) {
			highAnomalyValue = _HIGH_ANOMALY_AMPLITUDE;
		} else if ((5<=anomalyLikelihood) && (anomalyLikelihood<8)) {
			mediumAnomalyValue = _MEDIUM_ANOMALY_AMPLITUDE;
		} else {
			lowAnomalyValue = _LOW_ANOMALY_AMPLITUDE;
		}

		$scope.chartSeries['lowAnomaly'].data.shift();
		$scope.chartSeries['lowAnomaly'].data.push(lowAnomalyValue);
		$scope.chartSeries['mediumAnomaly'].data.shift();
		$scope.chartSeries['mediumAnomaly'].data.push(mediumAnomalyValue);
		$scope.chartSeries['highAnomaly'].data.shift();
		$scope.chartSeries['highAnomaly'].data.push(highAnomalyValue);
		$scope.chartSeries['metricValue'].data.shift();
		$scope.chartSeries['metricValue'].data.push(metricValue);

	}, 200);
*/

}]);




