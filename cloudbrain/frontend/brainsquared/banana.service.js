(function() {
  'use strict';

  angular.module('cloudbrain.brainsquared')
    .factory('Banana', ['eventEmitter', function(eventEmitter){

      var Banana = function (position) {
        // this.position = Math.random() >= 0.5 ? 'right' : 'left';
        this.position = position;
        this.map = THREE.ImageUtils.loadTexture( "../images/banana.png" );
        this.material = new THREE.SpriteMaterial( { map: this.map, color: 0xffffff, fog: true } );
        this.sprite = new THREE.Sprite( this.material );
        // this.bound = { x: 0.44, y: 0.5 }; //Scale 1
        // this.offset = { x: 0.28, y: 0.01 }; //Scale 1
        this.bound = { x: 0.85, y: 0.5 }; //Scale 2
        this.offset = { x: 0.07, y: 0.01 }; //Scale 2
        this.reset();
      };

      Banana.prototype.reset = function () {
        var x = this.position == 'left' ? -3.5 : 3.5;
        this.sprite.position.set(x, 4.2, 0.1);
        // this.sprite.position.set(x, -1, 0.1);
      };

      Banana.prototype.drop = function (rate) {
        rate = rate || 0.045;
        this.sprite.position.setY(this.sprite.position.y - rate);
      };

      return Banana;
  }]);

})();
