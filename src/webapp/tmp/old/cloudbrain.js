var GRAPH_URL,
    OCULUS_HOST,
    FULL_NAMESPACE,
    mini_graph,
    big_graph,
    selected,
    anomalous_datapoint;

var mini_data = [];
var big_data = [];
var initial = true;

var pull_data = function() {

    $.ajax({
        url: '/metrics',
        dataType: 'json',
        success: handle_data
    });
}

var handle_data = function(data){


    for (i in data) {
        metric_name = data[i];
 
        $.get("/api?metric=" + metric_name, function(d){
            console.log("/api?metric=" + FULL_NAMESPACE + "" + metric_name);
            data = JSON.parse(d)['results'];
        }); 

    }
}


var handle_data = function(data) {
    
    $('#metrics_listings').empty();

    for (i in data) {
        name = data[i];
        to_append = "<div class='sub'><div class='name'>" + name + " </div></a>&nbsp;&nbsp;";
        $('#metrics_listings').append(to_append);
    }

    /*
    if (initial) {
        selected = data[0][1];
        initial = false;
    }

    
    handle_interaction();
    */
}




var handle_interaction = function() {
    $('.sub').removeClass('selected');
    $('.sub:contains(' + selected + ')').addClass('selected');

    anomalous_datapoint = parseInt($($('.selected').children('.count')).text())
 
    $.get("/api?metric=" + selected, function(d){
        console.log("/api?metric=" + FULL_NAMESPACE + "" + selected);
        big_data = JSON.parse(d)['results'];
        big_graph.updateOptions( { 'file': big_data } );
        offset = (new Date().getTime() / 1000) - 3600;
        mini_data = big_data.filter(function (value) {
          return value[0] > offset;
        });
        mini_graph.updateOptions( { 'file': mini_data } );
    }); 


    $('#graph_title').html(selected);

    // Bleh, hack to fix up the layout on load
    $(window).resize();
}

$(function(){


    mini_graph = new Dygraph(document.getElementById("mini"), mini_data, {
        labels: [ 'Date', '' ], //hack to make the label / y axis prettier
        labelsDiv: document.getElementById('mini_label'),
        xAxisLabelWidth: 60,
        yAxisLabelWidth: 35,
        axisLabelFontSize: 10,
        rollPeriod: 1,
        drawXGrid: false,
        drawYGrid: false,
        interactionModel: {},
        pixelsPerLabel: 20,
        drawXAxis: false,
        drawAxesatZero: false,
        underlayCallback: function(canvas, area, g) {
            line = g.toDomYCoord(anomalous_datapoint);
            canvas.beginPath();
            canvas.moveTo(0, line);
            canvas.lineTo(canvas.canvas.width, line);
            canvas.lineWidth = 1;
            canvas.strokeStyle = '#ff0000';
            canvas.stroke();
        },
        axes : {
            x: {
                valueFormatter: function(ms) {
                return new Date(ms * 1000).strftime('%m/%d %H:%M') + ' ';
                },
            },
            y : {
                axisLineColor: 'white'
            },
            '' : {
                axisLineColor: 'white',
                axisLabelFormatter: function(x) {
                    return Math.round(x);
                }
            }
        },
    });

    big_graph = new Dygraph(document.getElementById("graph"), big_data, {
        labels: [ 'Date', '' ],
        labelsDiv: document.getElementById('big_label'),
        xAxisLabelWidth: 60,
        yAxisLabelWidth: 35,
        axisLabelFontSize: 9,
        rollPeriod: 2,
        drawXGrid: false,
        drawYGrid: false,
        interactionModel: {},
        pixelsPerLabel: 14,
        drawXAxis: false,
        underlayCallback: function(canvas, area, g) {
            line = g.toDomYCoord(anomalous_datapoint);
            canvas.beginPath();
            canvas.moveTo(0, line);
            canvas.lineTo(canvas.canvas.width, line);
            canvas.lineWidth = 1;
            canvas.strokeStyle = '#ff0000';
            canvas.stroke();
        },
        axes : {
            x: {
                valueFormatter: function(ms) {
                return new Date(ms * 1000).strftime('%m/%d %H:%M') + ' ';
                },
            },
            y : {
                axisLineColor: 'white'
            },
            '' : {
                axisLineColor: 'white',
                axisLabelFormatter: function(x) {
                    return Math.round(x);
                }
            }
        }
    });

    $.get('/app_settings', function(data){
        // Get the variables from settings.py
        data = JSON.parse(data);
        FULL_NAMESPACE = data['FULL_NAMESPACE'];
        GRAPH_URL = data['GRAPH_URL'];
        OCULUS_HOST = data['OCULUS_HOST'];

        // Get initial data after getting the host variables
        pull_data();

        $(window).resize();
    })

    // Update every thirty seconds
    window.setInterval(pull_data, 30000);

    // Set event listener
    $('.name').live('hover', function() {
        temp = $(this)[0].innerHTML;
        if (temp != selected) {
            selected = temp;
            handle_interaction();
        }
    })

    // Responsive graphs 
    $(window).resize(function() {
        resize_window();
    });
});

// I deeply apologize for this abomination
var resize_window = function() {
    mini_graph.resize($('#graph_container').width() - 7, ($('#graph_container').height() * (2/3)));
    big_graph.resize($('#graph_container').width() - 7, ($('#graph_container').height() * (1/3) - 5));
}

// Handle keyboard navigation
Mousetrap.bind(['up', 'down'], function(ev) {
    switch(ev.keyIdentifier) {
        case 'Up':
            next = $('.sub:contains(' + selected + ')').prev();
        break;

        case 'Down':
            next = $('.sub:contains(' + selected + ')').next();
        break;
    }

    if ($(next).html() != undefined) {
        selected = $(next).find('.name')[0].innerHTML;
        handle_interaction();
    } 

    return false;
}, 'keydown');





