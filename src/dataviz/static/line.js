var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// var parseDate = d3.time.format("%d-%b-%y").parse;

var x = d3.scale.linear()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line = d3.svg.line()
    .x(function(d) { return x(d[0]); })
    .y(function(d) { return y(d[1]); });

var svg = d3.select("#graph1").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


// generates a random number from standard Gaussian N(0,1)
function randn() {
    return ((Math.random() + Math.random() + Math.random() +
             Math.random() + Math.random() + Math.random()) - 3) * Math.sqrt(2);
}

// generates N random standard Gaussian numbers 
function nrandn(n) {
    var out = new Array(n);
    for(var i=0; i<n; i++) {
        out[i] = randn();
    }
    return out;
}

data = '';
function handle_data(d) {
    data = d["results"];
    console.log('handled!');
    console.log(data);

    // d = nrandn(1000);
    // data = d;
    // data = d.map(function(x, idx) {
    //     return {time: idx, data: x};
    // });

    // console.log(data);

    x.domain(d3.extent(data, function(d) { return d[0]; }));
    y.domain(d3.extent(data, function(d) { return d[1]; }));
    // y.range(d3.extent(data));

    // svg.append("g")
    //     .attr("class", "x axis")
    //     .attr("transform", "translate(0," + height + ")")
    //     .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
    // .attr("y", 6)
    // .attr("dy", ".71em")
        .style("text-anchor", "end")
    // .text("Price ($)");

    var path = svg.append("path")
        .datum(data)
        .attr("class", "line")
        .attr("d", line);
}

// The callback to this function is handle_data()
$.ajax({
    url: 'http://data.ebrain.io:1500/api?metric=marion.channel-0',
    dataType: 'jsonp',
    jsonp: false,
    jsonpCallback: "handle_data"
});



var idx = 1000;

// tick();

function tick() {
    
    data.push(randn());
    data.push(randn());
    data.push(randn());

    path.attr("d", line)
        .attr("transform", null)
        .transition()
        .duration(500)
        .ease("linear")
        .attr("transform", "translate(" + x(-3) + ",0)")
        .each("end", tick);

    data.shift();
    data.shift();
    data.shift();
    // x.domain(d3.extent(data, function(d) { return d.time; }));

    idx++;
    
    // svg.select("path").datum(data);
    console.log('updated?');
}

