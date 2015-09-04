    /* global angular */
(function () { 
  'use strict';

  angular.module('cloudbrain')

  .controller('HomeCtrl', ['$scope','$http','$interval','$log','apiService','dataService', 'API_URL',
  function ($scope , $http , $interval , $log , apiService , dataService, API_URL) {
    console.log('Home Controller');
    $scope.model = {
      deviceIds: [],
      deviceNames: ['muse', 'openbci'],
    };

    apiService.refreshDeviceIds().then(function(response) {
      console.log('response:', response);
      angular.copy(response.data, $scope.model.deviceIds);
    }, function(err){
      console.error('error:', err);
    });

    apiService.refreshPhysicalDeviceNames().then(function(response) {
      angular.copy(response.data, $scope.model.deviceNames);
    });
  
  }]);

})();
