var sensorName = 'acc';
var metricName = 'y';
$(function () {
    var values = [{metric_value: 0, timestamp: 0}];
    var _index = 0;
    
    var getData = function getData (start) {
          _c = "";
          if(start){
            _c = "&start=" + start;
          }
          return $.ajax({
          url: "http://localhost:5050/data?sensor="+ sensorName +"&metric=" + metricName+ _c + "&callback=?",
          async: false,
          dataType : 'JSON',
          }).done(function(json) {
            if(!json || json === "" || json.length <= 0){
                return;
            }
            values = [];
            for(var i = 0; i < json.length; i++){
                values.push({
                    metric_value: json[i].metric_value,
                    timestamp: json[i].timestamp,
                    anomaly: json[i].anomaly
                });
            }
            return json;
          });
    };
    
    
    $(document).on('ready', function() {
        
        var timeHorizon = 5 * 60 * 1000;
        getData(new Date().getTime() - timeHorizon).done(function () {
            drawGraph(sensorName, metricName);
        });
        // Getting data from the API every 2 seconds and pushing it into
        // the values array, we'll use the values in that array 
        // to populate the graph
        setInterval(getData, 1 * 1000);
    }); 

               
    var getPoints = function getPoints () {
        var rt;
        if(!values || values.length<1 || _index < 0){
            rt =  [new Date().getTime(), 0];
        } else {
            _index++;
            if(_index >= values.length ) {
                _index = values.length - 1;
            }
        }
        rt = [values[_index].timestamp || new Date().getTime(), values[_index].metric_value || 0];
        return rt;
    };


    var drawGraph = function drawGraph (metricName, axisName) {
        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });
        $('#container').highcharts('StockChart', {
            chart: {
                type: 'spline',
                animation: false, //Highcharts.svg, // don't animate in old IE
                marginRight: 10,
                events: {
                    load: function () {
                        // set up the updating of the chart each second
                        var series = this.series[0];
                        var xAxis = this.xAxis[0];
                        setInterval(function loadInterval () {
                            if(values[_index] && values[_index].anomaly===true){
                                xAxis.addPlotBand({
                                    color: '#FFAFAF',
                                    from: values[_index].timestamp - 500,
                                    to: values[_index].timestamp + 500
                                 });
                            }
                            series.addPoint(getPoints(), true, true);
                        }, 1000);
                    }
                }
            },
            
            rangeSelector: {
            buttons: [{
                count: 1,
                type: 'minute',
                text: '1M'
            }, {
                count: 2,
                type: 'minute',
                text: '2M'
            },{
                type: 'all',
                text: 'All'
            }],
            inputEnabled: false,
            selected: 0
        },

            title: {
                text: 'TI SensorTag - ' + metricName + '(' + axisName + ')'
            },
            
           

            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150,
                plotBands: []
            },
            yAxis: {
                title: {
                    text: 'Value'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },

            legend: {
                enabled: false
            },
            exporting: {
                enabled: false
            },
            series: [{
                name: 'TI SensorTag - ' + metricName + '(' + axisName + ')',
                data: (function () {
                    // generate an array of random data
                    var data = [];
                    for (i = 0; i < values.length; i++) {
                        data.push({
                            x: values[i].timestamp || new Date().getTime(),
                            y: values[i].metric_value || 0
                        });
                    }
                    return data;
                }())
            }]
        });
    };
});