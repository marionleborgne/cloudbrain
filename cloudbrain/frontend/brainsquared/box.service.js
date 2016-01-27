(function() {
  'use strict';

  angular.module('cloudbrain.brainsquared')
    .factory('Box', ['eventEmitter', function(eventEmitter){

      var Box = function (position) {
        this.map = THREE.ImageUtils.loadTexture( "../images/box.png" );
        this.material = new THREE.SpriteMaterial( { map: this.map, color: 0xffffff, fog: true } );
        this.sprite = new THREE.Sprite( this.material );
      };
      return Box;
  }]);

})();
