(function () {
	'use strict';

	angular.module('cloudbrain.rtchart', ['chart.js'])
		.config(['ChartJsProvider', function (ChartJsProvider) {
		  ChartJsProvider.setOptions({
		    colours: ['#FF5252', '#FF8A80'],
		    responsive: false
		  });
		  ChartJsProvider.setOptions('Line', {
		    datasetFill: false
		  });
		}])

})();
