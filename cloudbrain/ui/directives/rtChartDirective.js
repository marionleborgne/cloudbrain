(function(){
  'use strict';

  angular.module('cloudbrain')
    .directive('rtChart', ['RtChart', 'RtDataStream', function(RtChart, RtDataStream){

      var link = function(scope, element){

        scope.rtChartConfig = RtChart.chartConfig;

        scope.connectSocket = function() {
          RtDataStream.connect(
              function open(){
                console.log('connection open');
                RtDataStream.subscribe('eeg', function(msg) {
                  console.log('Message:', msg);

                    delete msg.timestamp;
                    for(var channel in msg){
                      RtChart.chartConfig.series[channel.split('_')[1]].data.push(msg[channel]);
                      if(RtChart.chartConfig.series[channel.split('_')[1]].data.length > 100){
                        RtChart.chartConfig.series[channel.split('_')[1]].data.shift();
                      }
                    }
                    scope.$digest();
                });
              },
              function close(){
                console.log('connection closed');
              });
        };
      };

      return {
        replace: true,
        restrict: 'E',
        scope: {
          rtChartConfig: '='
        },
        link: link,
        templateUrl: 'views/rtChartDirective.html'
      };

    }]);

})();
