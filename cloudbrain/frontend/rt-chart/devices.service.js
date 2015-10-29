(function() {
  'use strict';

  angular.module('cloudbrain.rtchart')
    .value('API_URL', 'http://apiserver.cloudbrain.rocks/api/v1.0')

    .factory('apiService', ['$http','$q', 'API_URL', '$log', function ($http , $q, API_URL, $log) {
      // Public service interface
      return {
        refreshPhysicalDeviceNames: refreshPhysicalDeviceNames
      };
      function refreshPhysicalDeviceNames() {
        return $http.jsonp(API_URL + '/metadata/devices?callback=JSON_CALLBACK');
      }
      function startDemoPublish() {
        //Specifically for the HTM Challenge
        return $http.get(API_URL + '/demo/publish');
      }
    }]);

})();
