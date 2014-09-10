var metrics;
var timeseries;


nv.addGraph(function() {
  var chart = nv.models.lineWithFocusChart();

  chart.xAxis
      .tickFormat(d3.format("d"));

  chart.yAxis
      .tickFormat(d3.format(',.2f'));

  chart.y2Axis
      .tickFormat(d3.format(',.2f'));

  datapoints = get_datapoints()

  d3.select('#chart svg')
      .datum(datapoints)
      .transition().duration(50)
      .call(chart);

  nv.utils.windowResize(chart.update);

  return chart;
});



/**************************************
 *  Cloudbrain data */
 

function get_datapoints() {

  load_data();
  datapoints = build_datapoints();
  return datapoints;
}

function load_metrics(){

    $.ajax({
      url : '/metrics',
      async: false,
      dataType : 'JSON',
      success : function(data) {
          metrics = data['results'];
      }
    })

    return metrics;
}

function load_data(){

  load_metrics();
  load_timeseries();

}

function load_timeseries(){

  timeseries = [];
  nbMetrics = metrics.length;
  for (i=0;i< nbMetrics;  i++) {
    metric_name = metrics[i];
    $.ajax({
      url : '/api?metric=' + metric_name,
      dataType : 'JSON',
      async: false,
      success : function(data) {
         timeseries.push(data['results']);
      }
    })
   
  }
  return timeseries;

}

function build_datapoints(){

    datapoints = []
    nbMetrics = metrics.length
      for (i=0; i< nbMetrics; i++) {
      datapoint = {key:metrics[i], values: timeseries[i]}
      datapoints.push(datapoint)
     }

    return datapoints;
}

