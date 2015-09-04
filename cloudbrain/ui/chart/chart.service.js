(function () { 
	'use strict';

	var chartMod = angular.module('cloudbrain')
  chartMod.value('API_URL', 'http://demo.apiserver.cloudbrain.rocks');

	chartMod.factory('apiService', ['$http','$q', 'API_URL', '$log', function ($http , $q, API_URL, $log) {
 		// Public service interface
	  return {
	    refreshDeviceIds: refreshDeviceIds,
	    refreshPhysicalDeviceNames: refreshPhysicalDeviceNames,
	  };
	  function refreshPhysicalDeviceNames() {
	    return $http.jsonp(API_URL + '/device_names?callback=JSON_CALLBACK');
	  }
	  function refreshDeviceIds() {
    	$log.log('refreshDeviceIds called');
    	var d = $q.defer();
    	$http.jsonp(API_URL + '/registered_devices?callback=JSON_CALLBACK').then(function(devices){
    		console.log('devices loaded:', devices);
    		d.resolve(devices);
    	}, function(err){
    		console.error('error refreshing device ids:', err);
    		d.reject(err.message || err);
    	});
      return d.promise;
    }
	}])
	//Data Service
	chartMod.factory('dataService',['$http','$interval', 'API_URL', function ($http, $interval, API_URL) {

	  var powerBandPromise = null;
	  var DATA_SPEED = 500;

	  function startPowerBand(deviceName, deviceId, callback) {
	    var curTimestamp = new Date().getTime();
	    if (!powerBandPromise) {
	      powerBandPromise = $interval(function() {
	        $http.jsonp(API_URL + '/power_bands?device_name=' + deviceName + 
	                    '&device_id=' + deviceId + 
	                    '&callback=JSON_CALLBACK&start=' + curTimestamp).then(function(response) {
	          // TODO: Update the curTimestamp with the latest timestamp from the
	          //       data currently returned.
	          callback(response.data);
	        });
	      }, DATA_SPEED);
	    }
	  }

	  function stopPowerBand() {
	    if (powerBandPromise) {
	      $interval.cancel(powerBandPromise);
	      powerBandPromise = null;
	    }
	  }

	  // Public service interface
	  return {
	    startPowerBand: startPowerBand,
	    stopPowerBand: stopPowerBand,
	  };

	}]);

})();

	