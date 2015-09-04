import config from '../config';
import _ from 'lodash';

let logger = {
	log(logData) {
		let msgArgs = buildMessageArgs(logData);
		if (config.envName == 'local') {
			console.log(logData);
		} else {
			console.log.apply(console, msgArgs);
		}
	},
	info(logData) {
		let msgArgs = buildMessageArgs(logData);
		if (config.envName == 'local') {
			console.info(logData);
		} else {
			console.info.apply(console, msgArgs);
		}
	},
	warn(logData) {
		let msgArgs = buildMessageArgs(logData);
		if (config.envName == 'local') {
			console.warn(logData);
		} else {
			console.warn.apply(console, msgArgs);
		}
	},
	debug(logData) {
		let msgArgs = buildMessageArgs(logData);
		if (config.envName == 'local') {
			console.log(logData);
		} else {
			console.log.apply(console, msgArgs);
		}
	},
	error(logData) {
		let msgArgs = buildMessageArgs(logData);
		if (config.envName == 'local') {
			console.error(logData);
		} else {
			console.error.apply(console, msgArgs);
			//TODO: Log to external logger
		}
	}
};

export default logger;

function buildMessageArgs(logData) {
	var msgStr = '';
	var msgObj = {};
	//TODO: Attach time stamp
	if (_.isObject(logData)) {
		if (_.has(logData, 'func')) {
			if (_.has(logData, 'obj')) {
				msgStr += '[' + logData.obj + '.' + logData.func + '()] ';
			} else if (_.has(logData, 'file')) {
				msgStr += '[' + logData.file + ' > ' + logData.func + '()] ';
			} else {
				msgStr += '[' + logData.func + '()] ';
			}
		}
		//Print each key and its value other than obj and func
		_.each(_.omit(_.keys(logData)), function(key, ind, list) {
			if (key != 'func' && key != 'obj') {
				if (key == 'description' || key == 'message') {
					msgStr += logData[key];
				} else if (_.isString(logData[key])) {
					// msgStr += key + ': ' + logData[key] + ', ';
					msgObj[key] = logData[key];
				} else {
					//Print objects differently
					// msgStr += key + ': ' + logData[key] + ', ';
					msgObj[key] = logData[key];
				}
			}
		});
		msgStr += '\n';
	} else if (_.isString(logData)) {
		msgStr = logData;
	}
	var msg = [msgStr, msgObj];

	return msg;
}
