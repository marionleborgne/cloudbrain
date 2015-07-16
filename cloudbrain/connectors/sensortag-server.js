var util = require('util');
var fs = require('fs');
var async = require('async');

var SensorTag = require('sensortag');

var context = require('rabbit.js').createContext();

var pubAcc = null;
var pubGyr = null;
var pubMag = null;

var fileName = 'data.csv';

context.on('ready', function() {
	pubAcc = context.socket('PUB');
	pubGyr = context.socket('PUB');
	pubMag = context.socket('PUB');

	pubAcc.connect('acc', function(){});
	pubGyr.connect('gyr', function(){});
	pubMag.connect('mag', function(){});
    });


SensorTag.discover(function(sensorTag) {
	console.log('discovered: ' + sensorTag);

	fileName = process.argv[2] || fileName;
	console.log('==> writing to file: ' + fileName);
	fileLine = "timestamp,x,y,z,g,raw_x,raw_y,raw_z\n";
	fs.appendFile(fileName, fileLine, function (err) {
		if (err) throw err;
		console.log('header: ' + fileLine);
	    });

	sensorTag.on('disconnect', function() {
		console.log('disconnected!');
		process.exit(0);

	});


	sensorTag.connectAndSetUp(function() {
		console.log('connectAndSetUp');
	
		sensorTag.enableAccelerometer(function() {
			console.log('enableAccelerometer');
			sensorTag.notifyAccelerometer(function(error){
				console.log("notifyAccelerometer");
			});

			sensorTag.on('accelerometerChange', function(x_raw, y_raw, z_raw) {
				raw = [x_raw, y_raw, z_raw];

				x = raw[0]-256*(raw[0]>127);
				y = -(raw[1]-256*(raw[1]>127));
				z = raw[2]-256*(raw[2]>127);

				g = Math.sqrt((x*x)+(y*y)+(z*z));
				pubAcc.write(JSON.stringify({x: x, y:y, z:z}), 'utf8');

				timestamp = new Date().getTime();
				fileLine = timestamp + ',' +  x + ',' + y + ',' + z + ',' + g + ',' + raw[0] + ',' + raw[1] + ',' + raw[2] + '\n';
				fs.appendFile(fileName, fileLine, function (err) {
					if (err) throw err;
					console.log(fileLine);
				    });
			});
		});


		sensorTag.enableGyroscope(function() {
			console.log('enableGyroscope');

			sensorTag.notifyGyroscope(function(error){
				console.log("notifyGyroscope");
			});

			sensorTag.on('gyroscopeChange', function(x_raw, y_raw, z_raw) {
				raw = [x_raw, y_raw, z_raw];
				x = raw[2]+256*raw[3]-65536*(raw[3]>127);
				y = raw[0]+256*raw[1]-65536*(raw[1]>127);
				z = raw[4]+256*raw[5]-65536*(raw[5]>127)
				pubGyr.write(JSON.stringify({x: x, y:y, z:z}), 'utf8');
	        });

		});

		sensorTag.enableMagnetometer(function() {
			console.log('enableMagnetometer');

			sensorTag.notifyMagnetometer(function(error){
				console.log("notifyMagnetometer");
			});

			sensorTag.on('magnetometerChange', function(x_raw, y_raw, z_raw) {
				raw = [x_raw, y_raw, z_raw];

				x = -(raw[0]+256*raw[1]-65536*(raw[1]>127));
				y = -(raw[2]+256*raw[3]-65536*(raw[3]>127));
				z = raw[4]+256*raw[5]-65536*(raw[5]>127);
				pubMag.write(JSON.stringify({x: x, y:y, z:z}), 'utf8');
          	});

		});

		setTimeout(function() {
			console.log('waiting ...');
		}, 2000);

	});

});	

