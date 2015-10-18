(function () {
  'use strict';

  angular.module('cloudbrain.calibration')
    .directive('calibration', ['$rootScope', '$interval', '$matter', 'apiService', 'Calibration', function($rootScope, $interval, $matter, apiService, Calibration){

      var link = function(scope, element){
        var elem = document.getElementById('draw-shapes');
        var params = { width: 2000, height: 2000 };
        var two = new Two(params).appendTo(elem);


        var circles = [];
        var num_circles = 8;
        var centerX = 75;
        var centerY = 75;
        var shift_right = 500;
        var center_align = 150;
        var left_align = 50;
        var right_align = 250;
        var top_row = 20;
        var mid_row = 150;
        var bot_row = 250;

        for (var i = 0; i < num_circles; i++){

         circles[i] = two.makeCircle(centerX, centerY, 50);
         //centerX += 150;
         circles[i].fill = 'red';
        }
        circles[0].translation.x = centerX + center_align;
        circles[1].translation.x = centerX + center_align;
        circles[2].translation.x = centerX + left_align;
        circles[3].translation.x = centerX + right_align;

        circles[4].translation.x = centerX + center_align + shift_right;
        circles[5].translation.x = centerX + center_align + shift_right;
        circles[6].translation.x = centerX + left_align + shift_right;
        circles[7].translation.x = centerX + right_align + shift_right;

        circles[0].translation.y = centerY + top_row;
        circles[1].translation.y = centerY + mid_row;
        circles[2].translation.y = centerY + bot_row;
        circles[3].translation.y = centerY + bot_row;

        circles[4].translation.y = centerY + top_row;
        circles[5].translation.y = centerY + mid_row;
        circles[6].translation.y = centerY + bot_row;
        circles[7].translation.y = centerY + bot_row;


        setInterval(function(){
         circles.forEach(function(circle){
           if (circle.fill === 'red'){
            circle.fill = 'orange';
           } else {
            circle.fill = 'red';
           }
           two.update();
         });
       }, 150);

        // Don't forget to tell two to render everything
        // to the screen
        two.update();
      };

      return {
        replace: true,
        restrict: 'E',
        scope: {},
        link: link,
        templateUrl: 'calibration/calibration-index.html'
      };

    }]);

})();
