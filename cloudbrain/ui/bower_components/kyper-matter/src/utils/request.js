import config from '../config';
import logger from './logger';
import token from './token';
import storage from './envStorage';
import superagent from 'superagent';

let request = {
	get(endpoint, queryData) {
		var req = superagent.get(endpoint);
		if (queryData) {
			req.query(queryData);
		}
		req = addAuthHeader(req);
		return handleResponse(req);
	},
	post(endpoint, data) {
		var req = superagent.post(endpoint).send(data);
		req = addAuthHeader(req);
		return handleResponse(req);
	},
	put(endpoint, data) {
		var req = superagent.put(endpoint).send(data);
		req = addAuthHeader(req);
		return handleResponse(req);
	},
	del(endpoint, data) {
		var req = superagent.put(endpoint).send(data);
		req = addAuthHeader(req);
		return handleResponse(req);
	}
};

export default request;

function handleResponse(req) {
	return new Promise((resolve, reject) => {
		req.end((err, res) => {
			if (!err) {
				// logger.log({description: 'Response:', response:res, func:'handleResponse', file: 'request'});
				return resolve(res.body);
			} else {
				if (err.status == 401) {
					logger.warn('Unauthorized. You must be signed into make this request.');
				}
				return reject(err);
			}
		});
	});
}
function addAuthHeader(req) {
	if (token.string) {
		req = req.set('Authorization', 'Bearer ' + token.string);
		logger.info({message: 'Set auth header', func: 'addAuthHeader', file: 'request'});
	}
	return req;
}
