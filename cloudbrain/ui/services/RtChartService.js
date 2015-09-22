(function(){
  'use strict';

  angular.module('cloudbrain')
    .factory('RtChart', ['RtDataStream', function(RtDataStream){

      var rtChartConfig = {
        options: {
          chart: {
            zoomType: 'x',
            type: 'spline'
          },
          tooltip: {
            enabled: false
          },
          legend: {
            enabled: true
          },
          rangeSelector: {
            buttons: [{
              count: 100,
              type: 'millisecond',
              text: '2S'
            }, {
              count: 300,
              type: 'millisecond',
              text: '30S'
            }, {
              type: 'all',
              text: 'All'
            }],
            selected: 0,
            inputEnabled: false
          },

          navigator: {
            enabled: true
          }
        },
        series: [],
        title: {
          text: 'EEG'
        },
        useHighStocks: true
      };

      var setChannelSeries = function(data){
        var keys = Object.keys(data);

        keys.forEach(function(key){
          if (key != 'timestamp'){
            for (var a=[],i=0;i<100;++i) a[i]=0;
            rtChartConfig.series.push({name: key, data: a, id: key});
          }
        });
      };

      setChannelSeries({
          channel_0: 0,
          channel_1: 0,
          channel_2: 0,
          channel_3: 0
        });

      return {
        chartConfig: rtChartConfig
      };

  }]);

})();
