/* global angular */
(function () { 'use strict';

angular.module('cloudbrain', ['ui.bootstrap', 'highcharts-ng'])


.factory('apiService',
        ['$http','$q' ,
function( $http , $q  ) {

    var API_URL = 'http://demo.apiserver.cloudbrain.rocks';

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


;

})();
