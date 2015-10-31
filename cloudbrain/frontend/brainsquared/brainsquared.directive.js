(function () {
  'use strict';

  angular.module('cloudbrain.brainsquared')
    .directive('brainsquared', ['$document', '$rootScope', '$interval', 'apiService', 'Minion', 'Banana', 'CollisionDetector', 'TargetTagger', 'Box',
      function($document, $rootScope, $interval, apiService, Minion, Banana, CollisionDetector, TargetTagger, Box){

      var link = function(scope, element, attrs){
        $document.on('keypress', function(e) {
          switch(e.which) {
            case 97: minion.step(0.3, 'left'); break;
            case 108: minion.step(0.3, 'right'); break;
          }
        });

        var scene = new THREE.Scene();
        var camera = new THREE.PerspectiveCamera( 100, window.innerWidth/window.innerHeight, 0.1, 1000 );
        var renderer = new THREE.WebGLRenderer({ alpha: true });
        renderer.setSize( window.innerWidth, window.innerHeight );
        renderer.setClearColor( 0xffffff, 1);
        element[0].appendChild( renderer.domElement );

        var generateNewBanana = function () {
          scene.remove( scope.banana.sprite );
          scope.banana = new Banana();
          scene.add( scope.banana.sprite );
          scope.minionBananaCollision = new CollisionDetector(minion, scope.banana);
        };

        var minion = new Minion();
        scene.add( minion.sprite );

        scope.banana = {};
        scope.score = 0;
        scope.target = '';

        // var grassMap = THREE.ImageUtils.loadTexture( "../images/grass.png" );
        // var grassMaterial = new THREE.SpriteMaterial( { map: grassMap, color: 0xffffff, fog: true } );
        // var grassSprite = new THREE.Sprite( grassMaterial );
        // scene.add( grassSprite );
        //
       var texture = THREE.ImageUtils.loadTexture( '../images/grass.png' );
       var backgroundMesh = new THREE.Mesh(
           new THREE.PlaneGeometry(50, 50, 0),
           new THREE.MeshBasicMaterial({
               map: texture
           }));

       backgroundMesh .material.depthTest = false;
       backgroundMesh .material.depthWrite = false;

       // Create your background scene
       var backgroundScene = new THREE.Scene();
       var backgroundCamera = new THREE.Camera();
       backgroundScene .add(backgroundCamera );
       backgroundScene .add(backgroundMesh );



        scope.$watch('minionBananaCollision.hasCollided()', function (newValue, oldValue) {
          if(newValue) {
            console.log('Collision detected!');
            generateNewBanana();
            scope.score += 1;
            minion.jump();
          }
        }, true);

        scope.$watch('banana.sprite.position.y', function (newValue, oldValue) {
          if(newValue <= -2) {
            generateNewBanana();
          }
        });

        camera.position.z = 3;

        var render = function () {
          requestAnimationFrame(render);
          renderer.render(backgroundScene , backgroundCamera );
          renderer.render(scene, camera);
        };

        // var minionBox = new Box();
        // var bananaBox = new Box();
        // scene.add( minionBox.sprite );
        // scene.add( bananaBox.sprite );
        //
        // generateNewBanana();
        // minionBox.sprite.position.copy(minion.sprite.position);
        // minionBox.sprite.position.setX(minion.sprite.position.x + minion.offset.x + minion.bound.x);
        //
        // bananaBox.sprite.position.copy(scope.banana.sprite.position);
        // bananaBox.sprite.position.setX(scope.banana.sprite.position.x + scope.banana.offset.x + scope.banana.bound.x);

        render();

        scope.startAll = function () {
          minion.start();
          generateNewBanana();
          scope.movement = $interval(function(){
            if(scope.banana) { scope.banana.drop(); }
            TargetTagger.tag(scope.minionBananaCollision.target());
          }, 50);
        };

        scope.resetAll = function () {
          minion.stop();
          minion.reset();
          scope.banana.reset();
          scope.score = 0;
          $interval.cancel(scope.movement);
        };

        scope.togglePlay = function () {
          scope.connected === true ? scope.resetAll() : scope.startAll();
          scope.connected = !scope.connected;
        };

      };

      return {
        replace: true,
        restrict: 'E',
        scope: {},
        link: link,
        templateUrl: 'brainsquared/brainsquared-index.html'
      };

    }]);

})();


// TODO:
// - Subscribe to 'classification' endpoint // brainsquare:openbci:classification
//
// - Update Minion position based on step size from classification
//
// - Reset bananas off-screen
// - Choose a random banana and drop it
// - Determine and publish target number
//
// - Increment score on banana/minion collision
