(function() {
  'use strict';

  angular.module('cloudbrain.brainsquared')
    .factory('CollisionDetector', ['eventEmitter', function(eventEmitter){

      var CollisionDetector = function (object_a, object_b) {
        //Positions
        this.pos_a = object_a.sprite.position;
        this.pos_b = object_b.sprite.position;
        //Offsets
        this.off_a = object_a.offset;
        this.off_b = object_b.offset;
        //Bounds
        this.bound_a = object_a.bound;
        this.bound_b = object_b.bound;
      };

      CollisionDetector.prototype.hasCollided = function () {
        if((this.pos_a.x + this.off_a.x < this.pos_b.x + this.off_b.x + this.bound_b.x &&
            this.pos_a.x + this.off_a.x + this.bound_a.x > this.pos_b.x + this.off_b.x) &&
           (this.pos_a.y + this.off_a.y < this.pos_b.y + this.off_b.y + this.bound_b.y) &&
           (this.pos_a.y + this.off_a.y + this.bound_a.y > this.pos_b.y + this.off_b.y)) {
          return true;
        }
        return false;
      };

      CollisionDetector.prototype.target = function () {
        if(this.pos_a.x + this.off_a.x + this.bound_a.x < this.pos_b.x + this.off_b.x){
          return 'right';
        }else if(this.pos_a.x + this.off_a.x > this.pos_b.x + this.off_b.x + this.bound_b.x){
          return 'left';
        }else {
          return 'baseline';
        }
      };

      return CollisionDetector;
  }]);

})();
