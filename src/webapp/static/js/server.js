var express = require('express');
var app = express();


var serialport = require('serialport');
var binary = require('binary');
var http = require('http');

var generate_data = true;

var port = '/dev/tty.usbmodem1411';
//port = '/dev/ttyACM0';

var raw_data = new Array(8);
for (var i=0; i<raw_data.length; i++) {
    raw_data[i] = new Array();
}

prev_data = new Buffer(0);

var start_time = new Date().getTime();
var data_times = new Array();

function formatData() {
    var out = new Array(8);
    var curr_time = new Date().getTime();
    // console.log(data_times);
    for(var i=0; i<8; i++) {
        var name = '' + (i+1);
        out[i] = {
            "start": data_times[0],
            "end": curr_time,
            "step": 4,
            "name": name,
            "value": raw_data[i]
        };
    }
    return out;
}

app.get('/data', function(req, res){
    var data = formatData();
    res.header("Access-Control-Allow-Origin", "*");
    res.header('Content-Type', 'application/json');
    res.end(JSON.stringify(data));
});
app.use(express.static(__dirname + '/static'));


app.listen(1337);

function pushData(d) {
    var t = new Date().getTime();
    data_times.push(t);

    for(var i=0; i<8; i++) {
        raw_data[i].push(d[i]);
    }

    if(raw_data[0].length >= 2000) {
        data_times.splice(0, 1);

        for(var i=0; i<8; i++) {
            raw_data[i].splice(0, 1);
        }
    }
}

function addPacket(packet) {

    //console.log(packet);
    var vars = binary.parse(packet)
        .word8lu('start')
        .word8lu('n_bytes')
        .word32lu('sample_index')
        .word32ls('channel_1')
        .word32ls('channel_2')
        .word32ls('channel_3')
        .word32ls('channel_4')
        .word32ls('channel_5')
        .word32ls('channel_6')
        .word32ls('channel_7')
        .word32ls('channel_8')
        .word8lu('end')
        .vars

    d = new Array(8);
    for(var i=0; i<8; i++) {
        d[i] = vars['channel_' + (i+1)] / Math.pow(2, 23);
    }

    if(vars.start == 0xA0 && vars.end == 0xC0) {
        pushData(d);
        for(var i=1; i<=8; i++) {
            raw_data[i-1].push(vars['channel_' + i] / Math.pow(2, 23))
            // vars['channel_' + i] /= Math.pow(2, 23)
        }
        //console.log(vars);
    }
}

function parseData(data) {
    if(data.length < 39) {
        prev_data = data;
        return;
    }

    var i = 0;
    while(i+39 < data.length) {
        if(data[i] == 0xA0) {
            var packet = data.slice(i, i+39);
            addPacket(packet);
            data = data.slice(i+39);
            i = 0;
        } else {
            i++;
        }
    }
    prev_data = data;
}

// generates a random number from standard Gaussian N(0,1)
function randn() {
    return ((Math.random() + Math.random() + Math.random() +
             Math.random() + Math.random() + Math.random()) - 3) * Math.sqrt(2);
}

// generates N random standard Gaussian numbers
function nrandn(n) {
    var out = new Array(n);
    for(var i=0; i<n; i++) {
        out[i] = randn() + 5;
    }
    return out;
}

if(!generate_data) {
    var SerialPort = serialport.SerialPort;
    var serialport = new SerialPort(port, {
        baudRate: 115200,
        dataBits: 8,
        parity: 'none',
        stopBits: 1,
        flowControl: false,
        parser: serialport.parsers.raw
    });


    serialport.on('open', function(){
        console.log('Serial Port Opend');
        serialport.on('data', function(data){
            // console.log(prev_data);
            // console.log(data);

            data = Buffer.concat([prev_data, data]);
            // console.log(data);
            parseData(data);
        });

        setTimeout(function() {
            serialport.write('b');
        }, 5000);
    });
} else {
    setInterval(function() {
        pushData(nrandn(8));
        pushData(nrandn(8));
        pushData(nrandn(8));
        pushData(nrandn(8));
    }, 16);
}



