var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ('value' in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError('Cannot call a class as a function'); } }

(function (global, factory) {
	typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory(require('lodash'), require('jwt-decode'), require('superagent')) : typeof define === 'function' && define.amd ? define(['lodash', 'jwt-decode', 'superagent'], factory) : global.Matter = factory(global._, global.jwtDecode, global.superagent);
})(this, function (_, jwtDecode, superagent) {
	'use strict';

	_ = 'default' in _ ? _['default'] : _;
	jwtDecode = 'default' in jwtDecode ? jwtDecode['default'] : jwtDecode;
	superagent = 'default' in superagent ? superagent['default'] : superagent;

	var config = {
		serverUrl: 'http://tessellate.elasticbeanstalk.com',
		tokenName: 'tessellate',
		tokenDataName: 'tessellate-tokenData'
	};

	var logger = {
		log: function log(logData) {
			var msgArgs = buildMessageArgs(logData);
			if (config.envName == 'local') {
				console.log(logData);
			} else {
				console.log.apply(console, msgArgs);
			}
		},
		info: function info(logData) {
			var msgArgs = buildMessageArgs(logData);
			if (config.envName == 'local') {
				console.info(logData);
			} else {
				console.info.apply(console, msgArgs);
			}
		},
		warn: function warn(logData) {
			var msgArgs = buildMessageArgs(logData);
			if (config.envName == 'local') {
				console.warn(logData);
			} else {
				console.warn.apply(console, msgArgs);
			}
		},
		debug: function debug(logData) {
			var msgArgs = buildMessageArgs(logData);
			if (config.envName == 'local') {
				console.log(logData);
			} else {
				console.log.apply(console, msgArgs);
			}
		},
		error: function error(logData) {
			var msgArgs = buildMessageArgs(logData);
			if (config.envName == 'local') {
				console.error(logData);
			} else {
				console.error.apply(console, msgArgs);
				//TODO: Log to external logger
			}
		}
	};

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
			_.each(_.omit(_.keys(logData)), function (key, ind, list) {
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

	var data = {};
	var storage = Object.defineProperties({
		/**
   * @description
   * Safley sets item to session storage.
   *
   * @param {String} itemName The items name
   * @param {String} itemValue The items value
   *
   */
		item: function item(itemName, itemValue) {
			return this.setItem(itemName, itemValue);
		},
		/**
   * @description
   * Safley sets item to session storage. Alias: item()
   *
   * @param {String} itemName The items name
   * @param {String} itemValue The items value
   *
   */
		setItem: function setItem(itemName, itemValue) {
			data[itemName] = itemValue;
			if (this.localExists) {
				//Convert object to string
				if (_.isObject(itemValue)) {
					itemValue = JSON.stringify(itemValue);
				}
				window.sessionStorage.setItem(itemName, itemValue);
			}
		},

		/**
   * @description
   * Safley gets an item from session storage. Alias: item()
   *
   * @param {String} itemName The items name
   *
   * @return {String}
   *
   */
		getItem: function getItem(itemName) {
			if (data[itemName]) {
				return data[itemName];
			} else if (this.localExists) {
				var itemStr = window.sessionStorage.getItem(itemName);
				//Check that str is not null before parsing
				if (itemStr) {
					var isObj = false;
					var itemObj = null;
					//Try parsing to object
					try {
						itemObj = JSON.parse(itemStr);
						isObj = true;
					} catch (err) {
						// logger.log({message: 'String could not be parsed.', error: err, func: 'getItem', obj: 'storage'});
						//Parsing failed, this must just be a string
						isObj = false;
					}
					if (isObj) {
						return itemObj;
					}
				}
				return itemStr;
			} else {
				return null;
			}
		},
		/**
   * @description
   * Safley removes item from session storage.
   *
   * @param {String} itemName - The items name
   *
   */
		removeItem: function removeItem(itemName) {
			//TODO: Only remove used items
			if (data[itemName]) {
				data[itemName] = null;
			}
			if (this.localExists) {
				try {
					//Clear session storage
					window.sessionStorage.removeItem(itemName);
				} catch (err) {
					logger.error({ description: 'Error removing item from session storage', error: err, obj: 'storage', func: 'removeItem' });
				}
			}
		},
		/**
   * @description
   * Safley removes item from session storage.
   *
   * @param {String} itemName the items name
   * @param {String} itemValue the items value
   *
   */
		clear: function clear() {
			//TODO: Only remove used items
			data = {};
			if (this.localExists) {
				try {
					//Clear session storage
					window.sessionStorage.clear();
				} catch (err) {
					logger.warn('Session storage could not be cleared.', err);
				}
			}
		}

	}, {
		localExists: {
			get: function get() {
				var testKey = 'test';
				if (typeof window != 'undefined' && typeof window.sessionStorage != 'undefined') {
					try {
						window.sessionStorage.setItem(testKey, '1');
						window.sessionStorage.removeItem(testKey);
						return true;
					} catch (err) {
						logger.error({ description: 'Error saving to session storage', error: err, obj: 'storage', func: 'localExists' });
						return false;
					}
				} else {
					return false;
				}
			},
			configurable: true,
			enumerable: true
		}
	});

	function decodeToken(tokenStr) {
		var tokenData = undefined;
		if (tokenStr && tokenStr != '') {
			try {
				tokenData = jwtDecode(tokenStr);
			} catch (err) {
				logger.error({ description: 'Error decoding token.', data: tokenData, error: err, func: 'decodeToken', file: 'token' });
				throw new Error('Invalid token string.');
			}
		}
		return tokenData;
	}
	var token = Object.defineProperties({
		save: function save(tokenStr) {
			this.string = tokenStr;
		},
		'delete': function _delete() {
			storage.removeItem(config.tokenName);
			storage.removeItem(config.tokenDataName);
			logger.log({ description: 'Token was removed.', func: 'delete', obj: 'token' });
		}
	}, {
		string: {
			get: function get() {
				return storage.getItem(config.tokenName);
			},
			set: function set(tokenStr) {
				logger.log({ description: 'Token was set.', token: tokenStr, func: 'string', obj: 'token' });
				this.data = jwtDecode(tokenStr);
				storage.setItem(config.tokenName, tokenStr);
			},
			configurable: true,
			enumerable: true
		},
		data: {
			get: function get() {
				if (storage.getItem(config.tokenDataName)) {
					return storage.getItem(config.tokenDataName);
				} else {
					return decodeToken(this.string);
				}
			},
			set: function set(tokenData) {
				if (_.isString(tokenData)) {
					var tokenStr = tokenData;
					tokenData = decodeToken(tokenStr);
					logger.info({ description: 'Token data was set as string. Decoding token.', token: tokenStr, tokenData: tokenData, func: 'data', obj: 'token' });
				} else {
					logger.log({ description: 'Token data was set.', data: tokenData, func: 'data', obj: 'token' });
					storage.setItem(config.tokenDataName, tokenData);
				}
			},
			configurable: true,
			enumerable: true
		}
	});

	var request = {
		get: function get(endpoint, queryData) {
			var req = superagent.get(endpoint);
			if (queryData) {
				req.query(queryData);
			}
			req = addAuthHeader(req);
			return handleResponse(req);
		},
		post: function post(endpoint, data) {
			var req = superagent.post(endpoint).send(data);
			req = addAuthHeader(req);
			return handleResponse(req);
		},
		put: function put(endpoint, data) {
			var req = superagent.put(endpoint).send(data);
			req = addAuthHeader(req);
			return handleResponse(req);
		},
		del: function del(endpoint, data) {
			var req = superagent.put(endpoint).send(data);
			req = addAuthHeader(req);
			return handleResponse(req);
		}
	};

	function handleResponse(req) {
		return new Promise(function (resolve, reject) {
			req.end(function (err, res) {
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
			logger.info({ message: 'Set auth header', func: 'addAuthHeader', file: 'request' });
		}
		return req;
	}

	var user = undefined;
	var endpoints = undefined;

	var Matter = (function () {
		/* Constructor
   * @param {string} appName Name of application
   */

		function Matter(appName, opts) {
			_classCallCheck(this, Matter);

			if (!appName) {
				logger.error({ description: 'Application name requires to use Matter.', func: 'constructor', obj: 'Matter' });
				throw new Error('Application name is required to use Matter');
			} else {
				this.name = appName;
			}
			if (opts) {
				this.options = opts;
			}
		}

		/* Endpoint getter
   *
   */

		_createClass(Matter, [{
			key: 'signup',

			/* Signup
    *
    */
			value: function signup(signupData) {
				return request.post(this.endpoint + '/signup', signupData).then(function (response) {
					logger.log({ description: 'Account request successful.', signupData: signupData, response: response, func: 'signup', obj: 'Matter' });
					if (_.has(response, 'account')) {
						return response.account;
					} else {
						logger.warn({ description: 'Account was not contained in signup response.', signupData: signupData, response: response, func: 'signup', obj: 'Matter' });
						return response;
					}
				})['catch'](function (errRes) {
					logger.error({ description: 'Error requesting signup.', signupData: signupData, error: errRes, func: 'signup', obj: 'Matter' });
					return Promise.reject(errRes);
				});
			}

			/** Login
    *
    */
		}, {
			key: 'login',
			value: function login(loginData) {
				var _this = this;

				if (!loginData || !loginData.password || !loginData.username) {
					logger.error({ description: 'Username/Email and Password are required to login', func: 'login', obj: 'Matter' });
					return Promise.reject({ message: 'Username/Email and Password are required to login' });
				}
				return request.put(this.endpoint + '/login', loginData).then(function (response) {
					if (_.has(response, 'data') && _.has(response.data, 'status') && response.data.status == 409) {
						logger.warn({ description: 'Account not found.', response: response, func: 'login', obj: 'Matter' });
						return Promise.reject(response.data);
					} else {
						logger.log({ description: 'Successful login.', response: response, func: 'login', obj: 'Matter' });
						if (_.has(response, 'token')) {
							_this.token.string = response.token;
						}
						if (_.has(response, 'account')) {
							_this.storage.setItem('currentUser', response.account);
						}
						return response.account;
					}
				})['catch'](function (errRes) {
					logger.error({ description: 'Error requesting login.', error: errRes, status: errRes.status, func: 'login', obj: 'Matter' });
					if (errRes.status == 409 || errRes.status == 400) {
						errRes = errRes.response.text;
					}
					return Promise.reject(errRes);
				});
			}

			/** Logout
    */
		}, {
			key: 'logout',
			value: function logout() {
				var _this2 = this;

				return request.put(this.endpoint + '/logout').then(function (response) {
					logger.log({ description: 'Logout successful.', response: response, func: 'logout', obj: 'Matter' });
					_this2.storage.removeItem('currentUser');
					_this2.token['delete']();
					return response;
				})['catch'](function (errRes) {
					logger.error({ description: 'Error requesting log out: ', error: errRes, func: 'logout', obj: 'Matter' });
					_this2.storage.removeItem('currentUser');
					_this2.token['delete']();
					return Promise.reject(errRes);
				});
			}
		}, {
			key: 'getCurrentUser',
			value: function getCurrentUser() {
				var _this3 = this;

				if (this.storage.item('currentUser')) {
					return Promise.resove(this.storage.item('currentUser'));
				} else {
					return request.get(this.endpoint + '/user').then(function (response) {
						//TODO: Save user information locally
						logger.log({ description: 'Current User Request responded.', responseData: response.data, func: 'currentUser', obj: 'Matter' });
						_this3.currentUser = response.data;
						return response.data;
					})['catch'](function (errRes) {
						logger.error({ description: 'Error requesting current user.', error: errRes, func: 'currentUser', obj: 'Matter' });
						return Promise.reject(errRes);
					});
				}
			}
		}, {
			key: 'updateProfile',

			/** updateProfile
    */
			value: function updateProfile(updateData) {
				var _this4 = this;

				if (!this.isLoggedIn) {
					logger.error({ description: 'No current user profile to update.', func: 'updateProfile', obj: 'Matter' });
					return Promise.reject({ message: 'Must be logged in to update profile.' });
				}
				//Send update request
				logger.warn({ description: 'Calling update endpoint.', endpoint: this.endpoint + '/user/' + this.token.data.username, func: 'updateProfile', obj: 'Matter' });
				return request.put(this.endpoint + '/user/' + this.token.data.username, updateData).then(function (response) {
					logger.log({ description: 'Update profile request responded.', responseData: response, func: 'updateProfile', obj: 'Matter' });
					_this4.currentUser = response;
					return response;
				})['catch'](function (errRes) {
					logger.error({ description: 'Error requesting current user.', error: errRes, func: 'updateProfile', obj: 'Matter' });
					return Promise.reject(errRes);
				});
			}

			/** updateProfile
    */
		}, {
			key: 'isInGroup',

			//Check that user is in a single group or in all of a list of groups
			value: function isInGroup(checkGroups) {
				var _this5 = this;

				if (!this.isLoggedIn) {
					logger.log({ description: 'No logged in user to check.', func: 'isInGroup', obj: 'Matter' });
					return false;
				}
				//Check if user is
				if (checkGroups && _.isString(checkGroups)) {
					var _ret = (function () {
						var groupName = checkGroups;
						//Single role or string list of roles
						var groupsArray = groupName.split(',');
						if (groupsArray.length > 1) {
							//String list of groupts
							logger.info({ description: 'String list of groups.', list: groupsArray, func: 'isInGroup', obj: 'Matter' });
							return {
								v: _this5.isInGroups(groupsArray)
							};
						} else {
							//Single group
							var groups = _this5.token.data.groups || [];
							logger.log({ description: 'Checking if user is in group.', group: groupName, userGroups: _this5.token.data.groups || [], func: 'isInGroup', obj: 'Matter' });
							return {
								v: _.any(groups, function (group) {
									return groupName == group.name;
								})
							};
						}
					})();

					if (typeof _ret === 'object') return _ret.v;
				} else if (checkGroups && _.isArray(checkGroups)) {
					//Array of roles
					//Check that user is in every group
					logger.info({ description: 'Array of groups.', list: checkGroups, func: 'isInGroup', obj: 'Matter' });
					return this.isInGroups(checkGroups);
				} else {
					return false;
				}
				//TODO: Handle string and array inputs
			}
		}, {
			key: 'isInGroups',
			value: function isInGroups(checkGroups) {
				var _this6 = this;

				//Check if user is in any of the provided groups
				if (checkGroups && _.isArray(checkGroups)) {
					return _.map(checkGroups, function (group) {
						if (_.isString(group)) {
							//Group is string
							return _this6.isInGroup(group);
						} else {
							//Group is object
							return _this6.isInGroup(group.name);
						}
					});
				} else if (checkGroups && _.isString(checkGroups)) {
					//TODO: Handle spaces within string list
					var groupsArray = checkGroups.split(',');
					if (groupsArray.length > 1) {
						return this.isInGroups(groupsArray);
					}
					return this.isInGroup(groupsArray[0]);
				} else {
					logger.error({ description: 'Invalid groups list.', func: 'isInGroups', obj: 'Matter' });
				}
			}
		}, {
			key: 'endpoint',
			get: function get() {
				var serverUrl = config.serverUrl;
				if (_.has(this, 'options') && this.options.localServer) {
					serverUrl = 'http://localhost:4000';
					logger.info({ description: 'LocalServer option was set to true. Now server url is local server.', url: serverUrl, func: 'endpoint', obj: 'Matter' });
				}
				if (this.name == 'tessellate') {
					//Remove url if host is server
					if (window && _.has(window, 'location') && window.location.host == serverUrl) {
						serverUrl = '';
						logger.info({ description: 'Host is Server, serverUrl simplified!', url: serverUrl, func: 'endpoint', obj: 'Matter' });
					}
				} else {
					serverUrl = config.serverUrl + '/apps/' + this.name;
					logger.info({ description: 'Server url set.', url: serverUrl, func: 'endpoint', obj: 'Matter' });
				}
				return serverUrl;
			}
		}, {
			key: 'currentUser',
			set: function set(userData) {
				logger.log({ description: 'Current User Request responded.', user: userData, func: 'currentUser', obj: 'Matter' });
				this.storage.setItem(userData);
			},
			get: function get() {
				if (this.storage.getItem('currentUser')) {
					return this.storage.getItem('currentUser');
				} else {
					return null;
				}
			}
		}, {
			key: 'storage',
			get: function get() {
				return storage;
			}

			/** updateProfile
    */
		}, {
			key: 'token',
			get: function get() {
				return token;
			}
		}, {
			key: 'utils',
			get: function get() {
				return { logger: logger, request: request, storage: storage };
			}
		}, {
			key: 'isLoggedIn',
			get: function get() {
				return this.token.string ? true : false;
			}
		}]);

		return Matter;
	})();

	;

	return Matter;
});
//# sourceMappingURL=matter.js.map