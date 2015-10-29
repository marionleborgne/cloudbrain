(function() {
  'use strict';

  angular.module('cloudbrain.brainsquared')
    .factory('ChartData', ['$q', 'RtDataStream', function($q, RtDataStream){

      var stream = {};

      var data = {
        mu: {
          left: {
            raw: [[]],
            class: [[]],
            classification: [[]]
          },
          right: {
            raw: [[]],
            class: [[]],
            classification: [[]]
          }
        }
      };

      function getSeries() {
        var staticSeries = ['mu'];
        return staticSeries;
      }

      function getLabels() {
        for (var a=[],i=0;i<100;++i) a[i]='';
        return a;
      }

      function getData(sensor, label) {
        return data[sensor][label];
      }

      function parseMessage(msg, sensor) {
        delete msg.timestamp;
        for(var label in msg){
          data.mu[sensor][label][0].push(msg[label]);
          if(data.mu[sensor][label][0].length > 300){
            data.mu[sensor][label][0].shift();
          }
        }
      }

      function start(callback) {
        stream = new RtDataStream('http://localhost:31415/rt-stream', 'openbci', 'brainsquared');

        stream.connect(
          function open(){
            console.log('Realtime Connection Open');
            stream.subscribe('muleft', function(msg) {
              parseMessage(msg, 'left');
            });
            stream.subscribe('muright', function(msg) {
              parseMessage(msg, 'right');
            });
          },
          function close(){
            console.log('Realtime Connection Closed');
          });
      }

      function stop() {
        stream.disconnect();
      }

      return {
        getSeries: getSeries,
        getLabels: getLabels,
        getData: getData,
        start: start,
        stop: stop
      };

  }]);

})();
