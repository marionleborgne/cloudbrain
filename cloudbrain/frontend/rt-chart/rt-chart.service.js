(function() {
  'use strict';

  angular.module('cloudbrain.rtchart')
    .factory('RtChart', ['$q', 'RtDataStream', function($q, RtDataStream){

      this.deviceType;
      this.deviceId;

      var stream = {};

      var data = [[],[],[],[]];

      function chartConfig() {
        var defaultConfig = {
          animation: false,
          animationSteps: 60,
          animationEasing: "easeOutQuart",
          showScale: true,
          scaleOverride: false,
          scaleSteps: null,
          scaleStepWidth: null,
          scaleStartValue: null,
          scaleLineColor: "rgba(0,0,0,.1)",
          scaleLineWidth: 1,
          scaleShowLabels: true,
          scaleLabel: "<%=value%>",
          scaleIntegersOnly: false,
          scaleBeginAtZero: true,
          scaleFontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
          scaleFontSize: 12,
          scaleFontStyle: "normal",
          scaleFontColor: "#666",
          responsive: true,
          maintainAspectRatio: true,
          showTooltips: true,
          customTooltips: false,
          tooltipEvents: ["mousemove", "touchstart", "touchmove"],
          tooltipFillColor: "rgba(0,0,0,0.8)",
          tooltipFontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
          tooltipFontSize: 14,
          tooltipFontStyle: "normal",
          tooltipFontColor: "#fff",
          tooltipTitleFontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
          tooltipTitleFontSize: 14,
          tooltipTitleFontStyle: "bold",
          tooltipTitleFontColor: "#fff",
          tooltipYPadding: 6,
          tooltipXPadding: 6,
          tooltipCaretSize: 8,
          tooltipCornerRadius: 6,
          tooltipXOffset: 10,
          tooltipTemplate: "<%if (label){%><%=label%>: <%}%><%= value %>",
          multiTooltipTemplate: "<%= value %>",
          scaleShowGridLines : true,
          scaleGridLineColor : "rgba(0,0,0,.05)",
          scaleGridLineWidth : 1,
          scaleShowHorizontalLines: true,
          scaleShowVerticalLines: true,
          bezierCurve : true,
          bezierCurveTension : 0.4,
          pointDot : false,
          pointDotRadius : 4,
          pointDotStrokeWidth : 1,
          pointHitDetectionRadius : 20,
          datasetStroke : true,
          datasetStrokeWidth : 2,
          datasetFill : false,
          legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>",
          onAnimationProgress: function(){},
          onAnimationComplete: function(){}
        };
        return defaultConfig;
      }

      function getSeries() {
        var staticSeries = ['channel_0', 'channel_1', 'channel_2', 'channel_3'];
        return staticSeries;
      }

      function getLabels() {
        for (var a=[],i=0;i<100;++i) a[i]='';
        return a;
      }

      function getData() {
        return data;
      }

      function setDeviceType(deviceType) {
        this.deviceType = deviceType;
      }

      function setDeviceId(deviceId) {
        this.deviceId = deviceId;
      }

      function start(callback) {
        stream = new RtDataStream('http://localhost:31415/rt-stream', this.deviceType, this.deviceId);

        stream.connect(
          function open(){
            console.log('Realtime Connection Open');
            stream.subscribe('eeg', function(msg) {
                delete msg.timestamp;
                for(var channel in msg){
                  data[channel.split('_')[1]].push(msg[channel]);
                  if(data[channel.split('_')[1]].length > 100){
                    data[channel.split('_')[1]].shift();
                  }
                }
            });
          },
          function close(){
            console.log('Realtime Connection Closed');
          });
      }

      function stop() {
        if(Object.keys(stream).length) {
          stream.disconnect();
        }
      }

      return {
        chartConfig: chartConfig,
        getSeries: getSeries,
        getLabels: getLabels,
        getData: getData,
        setDeviceType: setDeviceType,
        setDeviceId: setDeviceId,
        start: start,
        stop: stop
      };

  }]);

})();
