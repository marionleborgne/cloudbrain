'use strict';


var _GREEN = '#5cb85c';
var _RED = '#d9534f';
var _ORANGE = 'orange';
var _BLUE = "#337ab7";
var _PURPLE = "#800080";
var _HIGH_ANOMALY_AMPLITUDE = 6;
var _MEDIUM_ANOMALY_AMPLITUDE = 3;
var _LOW_ANOMALY_AMPLITUDE = 2;
var _POWER_BANDS = ['alpha', 'beta', 'gamma', 'theta', 'delta']
var _MUSE_METRICS = ['channel_0', 'channel_1', 'channel_2', 'channel_3']
var _OBCI_METRICS = ['channel_0', 'channel_1', 'channel_2', 'channel_3',
					'channel_4', 'channel_5', 'channel_6', 'channel_7']



// Angular App
var app = angular.module('cloudbrain', ["ui.bootstrap", "highcharts-ng"]);


// Main Screen Controller
app.controller('mainScreenController', ['$scope', '$interval', function ($scope, $interval) {

	// TODO: change that. hack to for the scope to refresh
	$interval(function () {}, 500);




	


	/*-------------*

	  METRICS

	*--------------*/

	// All metrics must have an ID
	$scope.files = [
			{
				name: 'Muse',
				metrics: {
					0: 'channel_0', 
					1:'channel_1', 
					2:'channel_2', 
					3: 'channel_3'
				}
			},
			{
				name: 'OpenBCI',
				metrics: {
					4: 'channel_0', 
					5: 'channel_1', 
					6: 'channel_2', 
					7: 'channel_3', 
					8: 'channel_4', 
					9: 'channel_5', 
					10: 'channel_6', 
					11: 'channel_7'}
			}
		]


	/*-------------*

	  CHART CONFIG

	*--------------*/

	
	var powerBandSeriesInit = {
		'alpha': 
		{
			type: 'column',
			name:'Alpha',
			color: _GREEN,
			data: [0]
		},
		'beta': 
		{
			type: 'column',
			name:'Beta',
			color: _ORANGE,
			data: [0]
		},  
		'gamma':               
		{
			type: 'column',
			name:'Gamma',
			color: _RED,
			data: [0]
		},
		'theta': 
		{
			type: 'column',
			name: 'Theta',
			color: _BLUE,
			data: [0]
		},
		'delta': 
		{
			type: 'column',
			name: 'Delta',
			color: _PURPLE,
			data: [0]
		}
	}


	$scope.powerBandSeries = {'Muse': {}, 'OpenBCI': {}};

	for (var i in _MUSE_METRICS){
		var metric = _MUSE_METRICS[i];
		$scope.powerBandSeries['Muse'][metric] = powerBandSeriesInit; 
	};
	for (var i in _OBCI_METRICS){
		var metric = _OBCI_METRICS[i];
		$scope.powerBandSeries['OpenBCI'][metric] = powerBandSeriesInit; 
	};	

	console.log($scope.powerBandSeries);


	/*-------------*

	  SHOW CHARTS

	*--------------*/

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



	// keep track of the charts we're showing
	$scope.chartsToShow = {};


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

	  CHARTS CONFIG

	*--------------*/



	$scope.powerBandsConfig = function(fileName, metricName) {

		return {

			series: $scope.powerBandSeries[fileName][metricName],
			title: {
				text: null,
			},
			credits: {
				enabled: false
			},
			loading: false,
			options:
			{

				chart: {
					polar: true,
					type: 'line'
				},

				tooltip:{
					enabled: true,
					animation: true
				},
				xAxis:{
					labels:{
						enabled: false
					},

				},
				yAxis:{
					lineWidth:0,
					gridLineWidth: 0,
					minorGridLineWidth: 0,
					max:15,
					min:0,
					labels:{
						enabled: false
					},
					title: ''
				},

				legend: {
					enabled: true,
				}
			}
		};

	};



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

		for (var k in _MUSE_METRICS){
			var metric = _MUSE_METRICS[k];
			for (var i in _POWER_BANDS){
				var powerBand = _POWER_BANDS[i];
				$scope.powerBandSeries['Muse'][metric][powerBand].data.shift();
				$scope.powerBandSeries['Muse'][metric][powerBand].data.push(record[metric][powerBand]['value']);
			};
		};


		for (var k in _OBCI_METRICS){
			var metric = _OBCI_METRICS[k];
			for (var i in _POWER_BANDS){
				var powerBand = _POWER_BANDS[i];
				$scope.powerBandSeries['OpenBCI'][metric][powerBand].data.shift();
				console.log(record[metric] + " : "+record[metric]['alpha']);
				$scope.powerBandSeries['OpenBCI'][metric][powerBand].data.push(record[metric][powerBand]['value']);
			};
		};

	});

}]);




