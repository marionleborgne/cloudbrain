(function() {
  'use strict';

  angular.module('cloudbrain.brainsquared')
    .factory('Banana', ['eventEmitter', function(eventEmitter){

      var Banana = function (position) {
        this.position = Math.random() >= 0.5 ? 'right' : 'left';
        this.map = THREE.ImageUtils.loadTexture( "../images/banana.png" );
        this.material = new THREE.SpriteMaterial( { map: this.map, color: 0xffffff, fog: true } );
        this.sprite = new THREE.Sprite( this.material );
        this.bound = { x: 0.44, y: 0.5 };
        this.offset = { x: 0.28, y: 0.01 };
        this.reset();
      };

      Banana.prototype.reset = function () {
        var x = this.position == 'left' ? -5 : 5;
        this.sprite.position.set(x, 4.5, 0.1);
      };

      Banana.prototype.drop = function (rate) {
        rate = rate || 0.045;
        this.sprite.position.setY(this.sprite.position.y - rate);
      };

      return Banana;
  }]);

})();
