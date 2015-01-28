angular.module('cogtech.central',[])
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
  _this.avg = {};
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
  _this.visitors = function visitors () {
    return $http.jsonp('http://cloudbrain.rocks/data/visitors?callback=JSON_CALLBACK')
    .then(function (response) {
      _this.totalVisitors = response.data;
      return response.data;
    });
  };
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
.directive('radarChart', function ($log, $avg) {
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
    // 1280 * 720
    $interval(function () {
      _this.obj = {};
      angular.forEach(_this.avgs, function (v, k) {
        if (!$avg.avg[k]) {
          return;
        }
        _this.avgs[k] = ($avg.avg[k].avg + 1 ) * 10;
      });
      _this.data[1] = {
        className : 'average',
        axes: [
          {axis: "Alpha", value: _this.avgs.alpha},
          {axis: "Beta", value: _this.avgs.beta},
          {axis: "Gamma", value: _this.avgs.gamma},
          {axis: "Theta", value: _this.avgs.theta},
          {axis: "Delta", value: _this.avgs.delta},
        ]
      };
      if(!$spacebrew.data[_this.muse] || !$spacebrew.data[_this.muse].alpha_absolute){
        return;
      }
      angular.forEach(_this.data[0].axes, function (v, k) {
        _this.data[0].value = ($spacebrew.data[_this.muse].alpha_absolute[_this.waves[k]] + 1 ) * 10;
      });
      _this.reDraw();
    }, 1000);
  };
  f.scope = {
  };
  f.controllerAs = "radar";
  f.template = "<p>Muse #{{radar.muse}}</p>";
  f.link = function(scope, element, attributes, controller) {
    $log.info(scope, element, attributes, controller);
    var data, chart, svg, color;
    controller.muse = attributes.muse || "5014";
    controller.data = [
      {
      className : controller.muse,
      axes: [
        // xOffset, yOffset
        {axis: "Alpha", value: 16},
        {axis: "Beta", value: 14},
        {axis: "Gamma", value: 18},
        {axis: "Theta", value: 14},
        {axis: "Delta", value: 14},
      ]
    },
    {
      className : 'average',
      axes: [
        // xOffset, yOffset
        {axis: "Alpha", value: 19},
        {axis: "Beta", value: 18},
        {axis: "Gamma", value: 19},
        {axis: "Theta", value: 14},
        {axis: "Delta", value: 20},
      ]
    }

    ];
    color = function color (i) {
      // return '#1f77b4';
      // https://github.com/mbostock/d3/wiki/Ordinal-Scales
      //$log.debug(d3.scale.category20c(i));
      return d3.scale.category10()(i);
    };
    chart = RadarChart.chart();
    chart.config({
      maxValue: 25,
      radians: 2 * Math.PI,
      axisLine: true,
      levels: 10,
      circles: true,
      radius: 5,
      w: 180,
      h: 180,
      ExtraWidthX: 100,
      ExtraWidthY: 100,
      color: d3.scale.category20()
    });
    svg = d3.select(element[0]).append('svg')
    .attr('width', 230)
    .attr('height', 230);
    svg.append('g').classed('focus', 1).datum(controller.data).call(chart);
    controller.reDraw = function reDraw () {
      svg.datum(controller.data).call(chart);
    };
  };
  return f;
})
.service('$spacebrew', function ($timeout, $log, $http) {
  var sb, _this;
  _this = this;
  _this.museIds = [
    '5014', '5008'
  ];
  _this.museClients = [];
  _this.client = {};
  _this.options = {
    name: 'data-visualization',
    server : 'cloudbrain.rocks',
    description : 'Main dashboard in room'
  };
  _this.waves = [
    'alpha_absolute',
    'beta_absolute',
    'gamma_absolute',
    'theta_absolute',
    'delta_absolute'
  ];
  _this.channels = [];
  angular.forEach(_this.museIds, function (client) {
    angular.forEach(_this.waves, function (wave) {
      _this.channels.push(wave + '-' +client);
    });
  });
  // object holds the data that comes from spacebrew
  // key is the muse-id, value is the array thing
  _this.data = {
    "5014" : {
      alpha: ['/muse/elements/alpha_absolute',0.1,0.1,0.1,0.1,5008],
      beta: ['beta',1,0,0,5014],
      gamma: ['gamma',0.2,0,0,5014],
      theta: ['theta',0.3,0,0,5014],
      delta: ['delta',-0.5,0,0,5014]
    }
  };
  sb = function init () {
    var sb;
    sb = new Spacebrew.Client(
      _this.options.server, _this.options.name, _this.options.description, {debug: true}
    );
    sb.extend(Spacebrew.Admin);
    sb.onStringMessage = function (name, value) {
      $log.info("message received", name, value);
      _this.data["5014"][name] = value.split(",");
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
    if(!_this.client || !_this.client.name) {
      $log.info('postponing creation of routes');
      return;
    }
    angular.forEach(_this.museIds, function (id) {
      angular.forEach(_this.waves, function(wave) {
        var url = "http://cloudbrain.rocks/link?pub_metric="+wave+"&"+
        "sub_metric="+wave+"-"+id+"&publisher="+client.name+
          "&subscriber="+_this.client.name+"&sub_ip="+_this.client.remoteAddress+"0&pub_ip="+client.remoteAddress;
        $http.jsonp(url + "&callback=JSON_CALLBACK").then(function (response) {
          $log.info(response.data);
        });
      });
      // sb.addRoute( client.name, client.remoteAdress, wave,
      //             _this.client.name, _this.client.remoteAdress, wave);
    });
  };

//cloudbrain.rocks/link?pub_metric=alpha_absolute&sub_metric=alpha_absolute&publisher=muse-5014&subscriber=data-visualization&sub_ip=8.31.67.210&pub_ip=127.0.0.1


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
