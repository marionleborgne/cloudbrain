(function() {
  'use strict';

  angular.module('cloudbrain.brainsquared')
    .factory('Minion', ['$timeout', 'RtDataStream', 'Accuracy', 'eventEmitter', function($timeout, RtDataStream, Accuracy, eventEmitter){

      var Minion = function () {
        this.map = THREE.ImageUtils.loadTexture( "../images/minion.png" );
        this.material = new THREE.SpriteMaterial( { map: this.map, color: 0xffffff, fog: true } );
        this.sprite = new THREE.Sprite( this.material );
        this.bound = { x: 0.57, y: 0.4 };
        this.offset = { x: 0.2, y: 0.01 };
        this.stream = {};
        this.reset();
      };

      Minion.prototype.reset = function () {
        this.sprite.position.set(0, -1.5, 0);
      };

      Minion.prototype.step = function (magnitude, direction) {
        magnitude = magnitude || 1;
        direction = direction || 'right';
        var stepSize = direction == 'right' ? magnitude : magnitude * -1;
        if(this.sprite.position.x > -5.7 && this.sprite.position.x < 5.7) {
          this.sprite.position.setX(this.sprite.position.x + stepSize);
        }else if(this.sprite.position.x <= -5.7) {
          this.sprite.position.setX(-5.6);
        }else if(this.sprite.position.x >= 5.7) {
          this.sprite.position.setX(5.6);
        }
      };

      Minion.prototype.start = function (callback) {
        var stream = this.stream = new RtDataStream('http://localhost:31415/rt-stream', 'module1', 'brainsquared');
        self = this;
        stream.connect(
          function open(){
            console.log('Realtime Connection Open');
            stream.subscribe('classification', function(msg) {
              if(msg.value !== 0){
                self.step(msg.value/10);
                Accuracy.step(msg.value/10);
              }
            });
          },
          function close(){
            console.log('Realtime Connection Closed');
          });
      };

      Minion.prototype.stop = function () {
        this.stream.disconnect();
      };

      Minion.prototype.jump = function () {
        var self = this.sprite.position;
        self.setY(-1);
        $timeout(function () {
          self.setY(-1.5);
        }, 80);
      };

      return Minion;
  }]);

})();
