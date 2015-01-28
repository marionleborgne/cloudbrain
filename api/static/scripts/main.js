angular.module('cogtech.central',[])
.directive('ctHeader', function () {
  var f = {};
  f.template = ''+
    '<img src="/static/img/brain.png" alt="cloud brain" class="logo">'+
    ' <h1>CloudBrain</h1>'+
    '<div style="height: 1.3em;" class="legends">'+
    ' <p style="float: left; margin: 0;"><span class="legend live">&nbsp;</span> Live Muse Data</p>'+
    '<p style="float: left; margin: 0; margin-left: 20px;"><span class="legend avg">&nbsp;</span> Average Across All Visitors</p>'+
    '</div>';
  f.scope = {};
  return f;
})
.controller('avgController', function ($interval, $avg) {
  var _this = this, rand, fetch, draw;
  _this.c = {};
  _this.r = {};
  _this.waves = ['alpha', 'beta', 'gamma', 'theta', 'delta'];

  _this.r.alpha = [14,19];
  _this.c.alpha = 0.1;

  _this.r.beta = [14,19];
  _this.c.beta = 0.4;

  _this.r.gamma = [14,19];
  _this.c.gamma = 0.5;

  _this.r.theta = [14,19];
  _this.c.theta = 0.3;

  _this.r.delta = [14,19];
  _this.c.delta = 0.2;

  _this.totalvisitors = 102;

  $interval(function intervalCheck () {
    fetch();
  }, 30000);

  $interval(function intervalDraw () {
    draw();
  }, 1000);
  draw = function draw () {
    angular.forEach(_this.waves, function (v) {
      _this.c[v] = rand(_this.c[v], _this.r[v]);
    });
  };

  fetch = function fetch () {
    $avg.fetch().then(function (data) {
      if (!data) {
        return;
      }
      angular.forEach(_this.waves, function (v) {
        _this.c[v] = data[v].avg;
        _this.r[v] = [data[v].avg - data[v].std, data[v].avg + data[v].std];
      });
    });
    $avg.visitors().then(function (data) {
      _this.totalvisitors = parseInt(data.visitors, 10);
    });
  };

  rand = function (e,r) {
    var a, v;
    if(true) {
      return e;
    }
    a = Math.random() * 1000;
    if(e > r[1] || e < r[0]) {
      v = r[0];
    }
    if (e === r[0]) {
      v = e += 1;
    }
    if (e === r[1]) {
      v = e += -1;
    }
    if (a < 400) {
      v = e +=1;
    } else {
      v = e += -1;
    }
    if(v <= 0 ) {
      v = 1.5;
    }
    return v;
  };
  draw();
  fetch();

})
.service('$avg', function ($http) {
  var _this = this;
  _this.avg = {"alpha": {"avg": 0.3}, "beta": {"avg": -0.2}, "delta": {"avg": 0.2}, "gamma": {"avg": 0.09}, "theta": {"avg": -0.27}};
  _this.totalvisitors = 0;
  _this.fetch = function fetch () {
    return $http.jsonp('http://cloudbrain.rocks/data/aggregates/fft?callback=JSON_CALLBACK')
    .then(function (response) {
      _this.avg = response.data;
      return response.data;
    }, function (response) {
      _this.avg = {};
    });
  };
  _this.fetch();
  _this.visitors = function visitors () {
    return $http.jsonp('http://cloudbrain.rocks/data/visitors?callback=JSON_CALLBACK')
    .then(function (response) {
      _this.totalVisitors = response.data;
      return response.data;
    });
  };
  _this.visitors();
})
.directive('ctBar', function ($interval) {
  var f = {};
  f.scope = {
    'value': '=',
  };
  f.template = "<div class='bar {{data.color}}' >"+
    "<!--<h2 class='title' data-ng-bind='data.title'></h2>-->" +
    "<div class='fill' ng-style=\"{'height': data.height , 'bottom' : data.bottom, 'top' : data.top }\">"+
    "<span ng-style=\"{'bottom': data.labelHeight }\">"+
    "{{data.title}} ({{data.value | double:2}} dB)</span></div>" +
    "</div>";
  f.controllerAs = "data";
  f.controller = function ($timeout, $interval) {
    var _this;
    _this = this;
    _this.bottom = '100px';
    $interval(function () {
      _this.calcHeight();
    }, 2000);
    _this.calcHeight = function calcHeight () {
      if (_this.value >= 0 ) {
        _this.bottom = '100px';
        _this.top = "";
        _this.height =  _this.value > 0 ? parseInt((_this.value * 10 ) * 0.8 ) + "px" : "10px";
        _this.labelHeight = _this.height;
      } else {
        _this.top = "100px";
        _this.bottom = "";
        _this.height =  ((+_this.value * -10 ) * 0.8 ) + "px";
        _this.labelHeight = _this.height;
      }
    };
    _this.calcHeight();
  };
  f.link = function (scope, elem, attrs, controller) {
    controller.title = attrs.title;
    controller.color = attrs.color;
    controller.value = scope.value * 10;
    $interval(function () {
      controller.value = scope.value * 10;
    }, 1000);
  };
  return f;
})
.filter('intg', function() {
  return function(input, zeroes) {
    return parseInt(input, zeroes);
  };
})
.filter('double', function () {
  return function(input) {
    return (input).toFixed(1);
  };
})
.controller('chartsController', function () {

})
// http://bl.ocks.org/mbostock/3048740 :(
// not using it
.directive('ctSpider', function ($log) {
  var f = {};
  f.controllerAs = "graph";
  f.controller = function () {
    var _this = this;
    _this.width = "300";
    _this.height= "300";
  };
  f.link = function(scope, elem, attrs, controller) {
    var formatDate, formatLabels, width, height, outerRadius, innerRadius,
    angle, radius, z, stack, nest, line, area, svg, labels;
    controller.waves = [];
    formatDate = d3.time.format("%a");
    labels = ['alpha', 'gamma', 'beta', 'theta'];
    formatLabels = function(d) {
      return labels[d];
    };

    width = controller.width;
    height = controller.height;
    outerRadius = height / 2 - 10;
    innerRadius = 0;

    angle = d3.time.scale()
    .range([0, 2 * Math.PI]);

    radius = d3.scale.linear()
    .range([innerRadius, outerRadius]);

    z = d3.scale.category20c();

    stack = d3.layout.stack()
    .offset("zero")
    .values(function(d) { return d.values; })
    .x(function(d) { return d.time; })
    .y(function(d) { return d.value; });

    nest = d3.nest()
    .key(function(d) { return d.key; });

    line = d3.svg.line.radial()
    .interpolate("cardinal-closed")
    .angle(function(d) { return angle(d.time); })
    .radius(function(d) { return radius(d.y0 + d.y); });

    area = d3.svg.area.radial()
    .interpolate("cardinal-closed")
    .angle(function(d) { return angle(d.y0); })
    .innerRadius(function(d) { return radius(d.y0); })
    .outerRadius(function(d) { return radius(d.y0 + d.y); });

    svg = d3.select(elem[0]).append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    controller.waves = [
      {"key" : "0", "values" : [
        {"key" : "alpha", "y" : 20, "y0" : 0},
        {"key" : "beta", "y" : 20, "y0" : 1},
        {"key" : "gamma", "y" : 20, "y0" : 2},
        {"key" : "theta", "y" : 20, "y0" : 3},
    ]},
    {"key" : "1", "values" : [
      {"key" : "alpha", "y" : 19, "y0" : 0},
      {"key" : "beta", "y" : 19, "y0" : 1},
      {"key" : "gamma", "y" : 19, "y0" : 2},
      {"key" : "theta", "y" : 19, "y0" : 3},
    ]},
    {"key" : "2", "values" : [
      {"key" : "beta", "y" : 19, "y0" : 0},
      {"key" : "beta", "y" : 19, "y0" : 1},
      {"key" : "beta", "y" : 19, "y0" : 2},
      {"key" : "beta", "y" : 19, "y0" : 3},
    ]}
    ];
    console.log(controller.waves);

    angle.domain([0, d3.max(controller.waves, function(d) { return 4; })]);
    radius.domain([0, d3.max(controller.waves, function(d) { return 30; })]);
    svg.selectAll(".layer")
    .data(controller.waves)
    .enter().append("path")
    .attr("class", "layer")
    .attr("d", function(d) { return area(d.values); })
    .style("fill", function(d, i) { return d.key === "2" ? "black" : z(i); });
    svg.selectAll(".axis")
      .data(d3.range(angle.domain()[1]))
      .enter().append("g")
      .attr("class", "axis")
      .attr("transform", function(d) { return "rotate(" + angle(d) * 180 / Math.PI + ")"; })
      .call(d3.svg.axis()
            .scale(radius.copy().range([-innerRadius, -outerRadius]))
            .orient("left"))
            .append("text")
            .attr("y",  (width / 2 ) - 20)
            .attr("dy", ".71em")
            .attr("text-anchor", "end")
            .text(function(d) { return formatLabels(d); });
  };
  return f;
})
.directive('radarChart', function ($log, $avg, muses) {
  // http://bl.ocks.org/nbremer/6506614
  var f = {};
  f.controller = function ($interval, $spacebrew) {
    var _this = this;
    _this.avgs = {
      'alpha': 1,
      'beta': 1,
      'gamma': 1,
      'theta': 1,
      'delta': 1
    };
    _this.waves = ['alpha_absolute', 'beta_absolute', 'gamma_absolute', 'theta_absolute','delta_absolute'];
    _this.data = [
      {
      className : 'average',
      axes: [
        {axis: "Alpha", value: 19},
        {axis: "Beta", value: 18},
        {axis: "Gamma", value: 19},
        {axis: "Theta", value: 14},
        {axis: "Delta", value: 20},
      ]
    },
    {
      className : _this.muse ? _this.muse.id : "",
      axes: [
        {axis: "Alpha", value: 80},
        {axis: "Beta", value: 70},
        {axis: "Gamma", value: 50},
        {axis: "Theta", value: 60},
        {axis: "Delta", value: 40},
      ]
    }
    ];

    // 1280 * 720
    $interval(function () {
      var temp = [];
      angular.forEach(_this.avgs, function (v, k) {
        if (!$avg.avg[k]) {
          return;
        }
        _this.avgs[k] = ($avg.avg[k].avg + 1 ) * 10;
      });
      _this.data[0] = {
        className : 'average',
        axes: [
          {axis: "Alpha", value: _this.avgs.alpha},
          {axis: "Beta", value: _this.avgs.beta},
          {axis: "Gamma", value: _this.avgs.gamma},
          {axis: "Theta", value: _this.avgs.theta},
          {axis: "Delta", value: _this.avgs.delta},
        ]
      };
      if(!$spacebrew.data[_this.muse.id] || !$spacebrew.data[_this.muse.id].alpha_absolute){
        // If there's no data for the current muse, leave it blank or in zero
        _this.data[1].axes = [
          {axis: "Alpha", value: 0},
          {axis: "Beta", value: 0},
          {axis: "Gamma", value: 0},
          {axis: "Theta", value: 0},
          {axis: "Delta", value: 0},
        ];
        return;
      }
      angular.forEach(_this.data[0].axes, function (v, k) {
        _this.data[1].axes[k].value = ($spacebrew.getValue(_this.muse.id, _this.waves[k]) + 1 ) * 10;
      });
      _this.reDraw();
    }, 1000);
  };
  f.scope = {
  };
  f.controllerAs = "radar";
  f.template = "<p> "+
    '<?xml version="1.0" encoding="utf-8"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg class="icon" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 64 64" enable-background="new 0 0 64 64" xml:space="preserve"><g>'+
    '<path ng-style="{fill: radar.muse.color}" d="M32.001,3.56C16.317,3.56,3.56,16.317,3.56,32c0,15.683,12.757,28.44,28.442,28.44                C47.683,60.44,60.44,47.683,60.44,32C60.44,16.317,47.683,3.56,32.001,3.56z M24.227,26.593l0.057-0.063                c0.232-0.168,0.345-0.432,0.303-0.708c-0.573-3.446-0.197-4.883-0.07-5.244c1.001-3.072,4.143-4.493,4.76-4.745                c0.131-0.052,0.374-0.125,0.62-0.163l0.073-0.017l0.505-0.027l0.004,0.031l0.117-0.011c0.104-0.011,0.204-0.025,0.329-0.051                l0.111-0.024c0.099,0.001,1.322,0.156,3.139,0.713l1.263,0.435c2.31,0.682,3.372,1.951,3.569,2.207                c1.85,2.095,1.354,5.259,0.896,6.958c-0.052,0.2-0.021,0.406,0.092,0.577l0.105,0.129c0.134,0.182,0.254,0.884-0.148,2.376                c-0.076,0.453-0.243,0.821-0.492,1.069c-0.092,0.101-0.156,0.229-0.179,0.374c-0.625,3.665-3.909,7.764-7.37,7.764                c-2.937,0-6.289-3.771-6.892-7.761c-0.023-0.149-0.085-0.28-0.188-0.393c-0.251-0.26-0.411-0.635-0.508-1.19                C24.029,27.785,24,26.944,24.227,26.593z M17.634,42.485c0.127-0.161,0.837-0.993,2.273-1.541c1.263-0.388,4.384-1.425,6.09-2.661                c0.08-0.044,0.159-0.127,0.224-0.194c0.158-0.17,0.399-0.429,0.685-0.694l0.159-0.151l0.162,0.152                c1.503,1.417,3.166,2.194,4.683,2.194c1.594,0,3.237-0.69,4.756-1.996l0.119-0.103l0.322,0.157                c0.288,0.264,0.786,0.626,1.018,0.736l0.296,0.145l-0.031,0.032l0.132,0.08c0.28,0.169,0.585,0.333,0.943,0.51                c0.361,0.159,0.663,0.277,0.976,0.379c0.264,0.086,1.668,0.558,3.265,1.296l0.305,0.092c1.562,0.598,2.256,1.429,2.325,1.516                c1.854,2.748,2.565,7.876,2.829,10.733c-4.843,3.933-10.935,6.098-17.162,6.098c-6.23,0-12.323-2.165-17.164-6.099                C15.098,50.316,15.803,45.204,17.634,42.485z"/></g></svg>'+
    "Visitor #{{radar.muse.number}}</p>";
    // LINK!
    f.link = function(scope, element, attributes, controller) {
      $log.info(scope, element, attributes, controller);
      var data, chart, svg, color;
      controller.muse = muses[attributes.muse || 0];
      // debugger;
      controller.data[0].className = controller.muse.id;
      color = function color (i) {
        // return '#1f77b4';
        // https://github.com/mbostock/d3/wiki/Ordinal-Scales
        //$log.debug(d3.scale.category20c(i));
        return d3.scale.category10()(i);
      };
      chart = RadarChart.chart();
      chart.config({
        maxValue: 23,
        radians: 2 * Math.PI,
        axisLine: true,
        levels: 10,
        circles: true,
        radius: 0,
        w: 145,
        h: 145,
        ExtraWidthX: 10,
        ExtraWidthY: 10,
        color: d3.scale.category20()
      });
      svg = d3.select(element[0]).append('svg')
      .attr('width', 150)
      .attr('height', 150);
      svg.append('g').classed('focus', 1).datum(controller.data).call(chart);
      controller.reDraw = function reDraw () {
        svg.datum(controller.data).call(chart);
      };
    };
  return f;
})
.service('muses', function () {
  return [
    {id: 5001, color: 'red', number: 1},
    {id: 5002, color: 'red', number: 2},
    {id: 5003, color: 'red', number: 3},
    {id: 5004, color: 'red', number: 4},
    {id: 5005, color: 'red', number: 5},
    {id: 5006, color: 'red', number: 6},
    {id: 5007, color: 'red', number: 7},
    {id: 5008, color: 'red', number: 8},
    {id: 5009, color: 'red', number: 9},
    {id: 5010, color: 'red', number: 10},
    {id: 5011, color: 'red', number: 11},
    {id: 5012, color: 'red', number: 12},
    {id: 5013, color: 'red', number: 13},
    {id: 5014, color: 'red', number: 14},
    {id: 5015, color: 'red', number: 15},
    {id: 5016, color: 'red', number: 16},
    {id: 5017, color: 'red', number: 17},
    {id: 5018, color: 'red', number: 18},
    {id: 5019, color: 'red', number: 19},
    {id: 5020, color: 'red', number: 20},
  ];
})
.service('$spacebrew', function ($timeout, $log, $http, muses) {
  var sb, _this;
  _this = this;

  _this.museClients = [];
  _this.client = {};
  _this.data = {};
  _this.options = {
    name: 'data-visualization',
    server : 'cloudbrain.rocks',
    description : 'Main dashboard in room',
    cloudbrain: 'cloudbrain.rocks'
  };
  _this.waves = [
    'alpha_absolute',
    'beta_absolute',
    'gamma_absolute',
    'theta_absolute',
    'delta_absolute'
  ];
  _this.channels = [];
  _this.getValue = function (muse_id, wave) {
    return (parseFloat(_this.data[muse_id][wave][2], 2) + parseFloat(_this.data[muse_id][wave][3], 2 ) ) / 2;
  };
  angular.forEach(muses, function (client) {
    angular.forEach(_this.waves, function (wave) {
      _this.channels.push(wave + '-' +client.id);
      _this.data[client.id] = {
        alpha_absolute: [0,0,1,0],
        beta_absolute:  [0,0,1,0],
        gamma_absolute:  [0,0,1,0],
        theta_absolute:  [0,0,1,0],
        delta_absolute:  [0,0,1,0]
      };
    });
  });
  // object holds the data that comes from spacebrew
  // key is the muse-id, value is the array thing
  sb = function init () {
    var sb;
    sb = new Spacebrew.Client(
      _this.options.server, _this.options.name, _this.options.description, {debug: true}
    );
    sb.extend(Spacebrew.Admin);
    sb.onStringMessage = function (name, value) {
      $log.info("message received", name, value);
      // TODO fix the shitty regex
      _this.data[name.replace(/.*_absolute-/,'')][name.replace(/-.*/,'')] = value.split(",");
    };
    sb.onOpen = function () {
      $log.info('connected to Spacebrew');
    };
    sb.onNewClient = function( client ) {
      $log.info(client);
      if(client.name && !!client.name.match(/muse/)) {
        _this.museClients.push(client);
        _this.addRoute();
      }
      if(client.name && client.name === _this.options.name) {
        _this.client = client;
        _this.addRoutes();
      }
    };
    sb.onRemoveClient(function (client) {
      $log.info(client);
    });
    angular.forEach(_this.channels, function (wave) {
      sb.addSubscribe(wave, "string");
    });
    sb.connect();
    return sb;
  }();

  _this.addRoutes = function addRoutes () {
    angular.forEach(_this.museClients, function (c) {
      _this.addRoute(c);
    });
  };

  _this.addRoute = function addRoute (client) {
    if(!client || !client.name){
      return;
    }
    if(!_this.client || !_this.client.name) {
      $log.info('postponing creation of routes');
      return;
    }
    angular.forEach(muses, function (muse) {
      angular.forEach(_this.waves, function(wave) {
        var url = "http://"+_this.options.cloudbrain+"/link?pub_metric="+wave+"&"+
        "sub_metric="+wave+"-"+muse.id+"&publisher="+client.name+
          "&subscriber="+_this.client.name+"&sub_ip="+_this.client.remoteAddress+"0&pub_ip="+client.remoteAddress;
        // TODO, could replace client.remoteAddress with ip of server
        $log.info(url);
        $http.jsonp(url + "&callback=JSON_CALLBACK").then(function (response) {
          $log.info(response.data);
        });
      });
    });
  };

});
// http://cloudbrain.rocks/

// http://spacebrew.github.io/spacebrew/admin/admin.html?server=cloudbrain.rocks
// Request
// GET request on /link with the following parameters:
// publisher : The input data coming from the hardware (Muse headset for example).
// subscriber : Set it to 'cloudbrain' to keep historical data. Can also be set to your spacebrew client to get live data.
// pub_metric : The publisher name of the metric you want to route. See the Muse Metrics section below for the complete list.
// sub_metric : The subscriber name of the metric you want to route.
// Sample Request
// GET
//
// http://cloudbrain.rocks/link?pub_metric=beta_absolute&sub_metric=beta_absolute&publisher=muse-001&subscriber=data-visualization
