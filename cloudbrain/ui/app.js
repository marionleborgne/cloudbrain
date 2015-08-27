/* global angular */
(function () { 'use strict';

angular.module('cloudbrain', ['ui.bootstrap', 'highcharts-ng'])


.factory('apiService',
        ['$http','$q' ,
function( $http , $q  ) {

    var API_URL = 'http://demo.apiserver.cloudbrain.rocks';

    function refreshDeviceNames() {
        return $http.jsonp(API_URL + '/device_names?callback=JSON_CALLBACK');
    }

    // Public service interface
    return {
        refreshDeviceNames: refreshDeviceNames,
    };


}])


;

})();
