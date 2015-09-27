/* global angular */
(function () { 'use strict';

var API_URL = 'http://apiserver.cloudbrain.rocks';

angular.module('cloudbrain', ['ui.bootstrap', 'highcharts-ng'])


.factory('apiService',
        ['$http','$q' ,
function( $http , $q  ) {

    function refreshPhysicalDeviceNames() {
        return $http.jsonp(API_URL + '/device_names?callback=JSON_CALLBACK');
    }

    function refreshDeviceIds() {
        return $http.jsonp(API_URL + '/registered_devices?callback=JSON_CALLBACK');
    }

    // Public service interface
    return {
        refreshDeviceIds: refreshDeviceIds,
        refreshPhysicalDeviceNames: refreshPhysicalDeviceNames,
    };


}])


.factory('dataService',
        ['$http','$interval' ,
function( $http , $interval  ) {

    var powerBandPromise = null;
    var DATA_SPEED = 500;

    function startPowerBand(deviceName, deviceId, callback) {
        var curTimestamp = new Date().getTime();
        if (!powerBandPromise) {
            powerBandPromise = $interval(function() {
                $http.jsonp(API_URL + '/power_bands?device_name=' + deviceName +
                            '&device_id=' + deviceId + 
                            '&callback=JSON_CALLBACK&start=' + curTimestamp).then(
                function(response) {
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


}])



;

})();
