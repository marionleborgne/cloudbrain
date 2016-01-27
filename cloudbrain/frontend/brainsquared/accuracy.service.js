(function() {
  'use strict';

  angular.module('cloudbrain.brainsquared')
    .factory('Accuracy', ['$rootScope', 'eventEmitter', function($rootScope, eventEmitter){

      var Accuracy = function () {
        this.accurateSteps = 0;
        this.totalSteps = 0;
        this.target = '';
      };

      Accuracy.prototype.get = function () {
        var accuracyScore = (this.accurateSteps/this.totalSteps).toFixed(2) || 0;
        if ( isNaN(accuracyScore) ) { accuracyScore = 0 };
        return {
          accuracyScore: accuracyScore,
          accurateSteps: this.accurateSteps,
          totalSteps: this.totalSteps
        };
      };

      Accuracy.prototype.step = function (step) {
        this.totalSteps += 1;
        if((step < 0 && this.target == 'left') || (step > 0 && this.target == 'right')){
          this.accurateSteps += 1;
        }
        $rootScope.$broadcast('accuracyUpdated', this.get());
      };

      Accuracy.prototype.setTarget = function (target) {
        this.target = target;
      };

      Accuracy.prototype.reset = function () {
        this.accurateSteps = 0;
        this.totalSteps = 0;
        this.target = '';
      };

      return new Accuracy();
  }]);

})();
