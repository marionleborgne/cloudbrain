(function() {
  'use strict';

  angular.module('cloudbrain.brainsquared')
    .factory('AnalysisModule', ['MODULE_URL', 'STREAM_MODE', '$http', 'eventEmitter', function(MODULE_URL, STREAM_MODE, $http, eventEmitter){

      var AnalysisModule = function (module_type, device_type) {
        this.module_type = module_type;
        this.device_type = device_type;
        this.module_id = '';
        this.lastTag = '';
      };

      AnalysisModule.prototype.create = function () {
        var self = this;
        var body = {
          module_type: self.module_type,
          device_type: self.device_type
        };
        console.log(body);
        return $http.post(MODULE_URL, body).then(function (response) {
          console.log(response);
          self.module_id = response.data.id;
        }, function (response) {
          console.log("AnalysisModule.create Error", response);
        });
      };

      AnalysisModule.prototype.tag = function (tag) {
        var body = {
          timestamp: new Date().getTime(),
          value: tag
        };

        var tagSuccess = function (response) {
          console.log('Success', response);
        };

        var tagError = function (response) {
          console.log('Error', response);
        };

        if(this.lastTag != tag || STREAM_MODE === true){
          $http.post(MODULE_URL + '/' + this.module_id + '/tag' , body).then(tagSuccess, tagError);
        }

        this.lastTag = tag;
      };

      return AnalysisModule;
  }]);

})();
