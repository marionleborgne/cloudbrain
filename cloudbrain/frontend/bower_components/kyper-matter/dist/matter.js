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
		tokenDataName: 'tessellate-tokenData',
		tokenUserDataName: 'tessellate-currentUser'
	};

	//Set default log level to debug
	var logLevel = 'debug';
	//Set log level from config
	if (config.logLevel) {
		logLevel = config.logLevel;
	}

	var logger = {
		log: function log(logData) {
			var msgArgs = buildMessageArgs(logData);
			if (config.envName == 'production') {
				runConsoleMethod('log', msgArgs);
			} else {
				runConsoleMethod('log', msgArgs);
			}
		},
		info: function info(logData) {
			var msgArgs = buildMessageArgs(logData);
			if (config.envName == 'production') {
				runConsoleMethod('info', msgArgs);
			} else {
				runConsoleMethod('info', msgArgs);
			}
		},
		warn: function warn(logData) {
			var msgArgs = buildMessageArgs(logData);
			if (config.envName == 'production') {
				runConsoleMethod('warn', msgArgs);
			} else {
				runConsoleMethod('warn', msgArgs);
			}
		},
		debug: function debug(logData) {
			var msgArgs = buildMessageArgs(logData);
			if (config.envName == 'production') {
				// runConsoleMethod('debug', msgArgs);
				//Do not display console debugs in production
			} else {
					runConsoleMethod('debug', msgArgs);
				}
		},
		error: function error(logData) {
			var msgArgs = buildMessageArgs(logData);
			if (config.envName == 'production') {
				//TODO: Log to external logger
				runConsoleMethod('error', msgArgs);
			} else {
				runConsoleMethod('error', msgArgs);
			}
		}
	};

	function runConsoleMethod(methodName, methodData) {
		//Safley run console methods or use console log
		if (methodName && console[methodName]) {
			return console[methodName].apply(console, methodData);
		} else {
			return console.log.apply(console, methodData);
		}
	}
	function buildMessageArgs(logData) {
		var msgStr = '';
		var msgObj = {};
		//TODO: Attach time stamp
		//Attach location information to the beginning of message
		if (_.isObject(logData)) {
			if (logLevel == 'debug') {
				if (_.has(logData, 'func')) {
					if (_.has(logData, 'obj')) {
						//Object and function provided
						msgStr += '[' + logData.obj + '.' + logData.func + '()]\n ';
					} else if (_.has(logData, 'file')) {
						msgStr += '[' + logData.file + ' > ' + logData.func + '()]\n ';
					} else {
						msgStr += '[' + logData.func + '()]\n ';
					}
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

	var domUtil = {
		/**
   * @description
   * Appends given css source to DOM head.
   *
   * @param {String} src - url src for css to append
   *
   */
		loadCss: function loadCss(src) {
			if (!document) {
				logger.error({ description: 'Document does not exsist to load assets into.', func: 'loadCss', obj: 'dom' });
				throw new Error('Document object is required to load assets.');
			} else {
				var css = document.createElement('link');
				css.rel = 'stylesheet';
				css.type = 'text/css';
				css.href = src;
				document.getElementsByTagName('head')[0].insertBefore(css, document.getElementsByTagName('head')[0].firstChild);
				logger.log({ description: 'CSS was loaded into document.', element: css, func: 'loadCss', obj: 'dom' });
				return css; //Return link element
			}
		},
		/**
   * @description
   * Appends given javascript source to DOM head.
   *
   * @param {String} src - url src for javascript to append
   *
   */
		loadJs: function loadJs(src) {
			if (window && !_.has(window, 'document')) {
				logger.error({ description: 'Document does not exsist to load assets into.', func: 'loadCss', obj: 'dom' });
				throw new Error('Document object is required to load assets.');
			} else {
				var js = window.document.createElement('script');
				js.src = src;
				js.type = 'text/javascript';
				window.document.getElementsByTagName('head')[0].appendChild(js);
				logger.log({ description: 'JS was loaded into document.', element: js, func: 'loadCss', obj: 'dom' });
				return js; //Return script element
			}
		},
		/**
   * @description
   * Appends given javascript source to DOM head.
   *
   * @param {String} src - url src for javascript to append
   *
   */
		asyncLoadJs: function asyncLoadJs(src) {
			if (!_.has(window, 'document')) {
				logger.error({ description: 'Document does not exsist to load assets into.', func: 'loadCss', obj: 'dom' });
				throw new Error('Document object is required to load assets.');
			} else {
				var js = window.document.createElement('script');
				js.src = src;
				js.type = 'text/javascript';
				window.document.getElementsByTagName('head')[0].appendChild(js);
				logger.log({ description: 'JS was loaded into document.', element: js, func: 'loadCss', obj: 'dom' });
				return new Promise(function (resolve, reject) {
					window.setTimeout(resolve, 30);
				});
			}
		}
	};

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
			//Remove string token
			storage.removeItem(config.tokenName);
			//Remove user data
			storage.removeItem(config.tokenDataName);
			logger.log({ description: 'Token was removed.', func: 'delete', obj: 'token' });
		}
	}, {
		string: {
			get: function get() {
				return storage.getItem(config.tokenName);
			},
			set: function set(tokenData) {
				var tokenStr = undefined;
				//Handle object being passed
				if (!_.isString(tokenData)) {
					//Token is included in object
					logger.log({ description: 'Token data is not string.', token: tokenData, func: 'string', obj: 'token' });

					if (_.isObject(tokenData) && _.has(tokenData, 'token')) {
						tokenStr = tokenData.token;
					} else {
						//Input is either not an string or object that contains nessesary info
						logger.error({ description: 'Invalid value set to token.', token: tokenData, func: 'string', obj: 'token' });
						return;
					}
				} else {
					tokenStr = tokenData;
				}
				logger.log({ description: 'Token was set.', token: tokenData, tokenStr: tokenStr, func: 'string', obj: 'token' });
				storage.setItem(config.tokenName, tokenStr);
				this.data = jwtDecode(tokenStr);
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
						logger.warn({ description: 'Unauthorized. You must be signed into make this request.', func: 'handleResponse' });
					}
					if (err && err.response) {
						return reject(err.response.text);
					}
					logger.warn({ description: 'Unauthorized. You must be signed into make this request.', error: err, func: 'handleResponse' });
					return reject(err);
				}
			});
		});
	}
	function addAuthHeader(req) {
		if (token.string) {
			req = req.set('Authorization', 'Bearer ' + token.string);
			console.info({ message: 'Set auth header', func: 'addAuthHeader', file: 'request' });
		}
		return req;
	}

	// import hello from 'hellojs'; //Modifies objects to have id parameter?

	// import hello from 'hellojs'; //After es version of module is created
	//Private object containing clientIds
	var clientIds = {};

	var ProviderAuth = (function () {
		function ProviderAuth(actionData) {
			_classCallCheck(this, ProviderAuth);

			this.app = actionData.app ? actionData.app : null;
			this.redirectUri = actionData.redirectUri ? actionData.redirectUri : 'redirect.html';
			this.provider = actionData.provider ? actionData.provider : null;
		}

		_createClass(ProviderAuth, [{
			key: 'loadHello',
			value: function loadHello() {
				//Load hellojs script
				//TODO: Replace this with es6ified version
				if (window && !window.hello) {
					return domUtil.asyncLoadJs('https://s3.amazonaws.com/kyper-cdn/js/hello.js');
				} else {
					return Promise.resolve();
				}
			}
		}, {
			key: 'helloLoginListener',
			value: function helloLoginListener() {
				//Login Listener
				window.hello.on('auth.login', function (auth) {
					logger.info({ description: 'User logged in to google.', func: 'loadHello', obj: 'Google' });
					// Call user information, for the given network
					window.hello(auth.network).api('/me').then(function (r) {
						// Inject it into the container
						//TODO:Send account informaiton to server
						var userData = r;
						userData.provider = auth.network;
						//Login or Signup endpoint
						return request.post(this.endpoint + '/provider', userData).then(function (response) {
							logger.log({ description: 'Provider request successful.', response: response, func: 'signup', obj: 'GoogleUtil' });
							return response;
						})['catch'](function (errRes) {
							logger.error({ description: 'Error requesting login.', error: errRes, func: 'signup', obj: 'Matter' });
							return Promise.reject(errRes);
						});
					});
				});
			}
		}, {
			key: 'initHello',
			value: function initHello() {
				var _this = this;

				return this.loadHello().then(function () {
					return request.get(_this.app.endpoint + '/providers').then(function (response) {
						logger.log({ description: 'Provider request successful.', response: response, func: 'signup', obj: 'ProviderAuth' });
						var provider = response[_this.provider];
						logger.warn({ description: 'Provider found', provider: provider, func: 'login', obj: 'ProviderAuth' });
						if (!provider) {
							logger.error({ description: 'Provider is not setup. Visit tessellate.kyper.io to enter your client id for ' + _this.provider, provider: _this.provider, clientIds: clientIds, func: 'login', obj: 'ProviderAuth' });
							return Promise.reject({ message: 'Provider is not setup.' });
						}
						logger.warn({ description: 'Providers config built', providersConfig: response, func: 'login', obj: 'ProviderAuth' });
						return window.hello.init(response, { redirect_uri: 'redirect.html' });
					})['catch'](function (errRes) {
						logger.error({ description: 'Getting application data.', error: errRes, func: 'signup', obj: 'Matter' });
						return Promise.reject(errRes);
					});
				});
			}
		}, {
			key: 'login',
			value: function login() {
				var _this2 = this;

				//Initalize Hello
				return this.initHello().then(function () {
					return window.hello.login(_this2.provider);
				});
			}
		}, {
			key: 'signup',
			value: function signup() {
				var _this3 = this;

				//Initalize Hello
				// if (!_.has(clientIds, this.provider)) {
				// 	logger.error({description: `${this.provider} is not setup as a provider on Tessellate. Please visit tessellate.kyper.io to enter your provider information.`, provider: this.provider, clientIds: clientIds, func: 'login', obj: 'ProviderAuth'});
				// 	return Promise.reject();
				// }
				//TODO: send info to server
				return this.initHello().then(function () {
					return window.hello.login(_this3.provider);
				}, function (errRes) {
					logger.error({ description: 'Error signing up.', error: errRes, func: 'signup', obj: 'Matter' });
					return Promise.reject({ message: 'Error signing up.' });
				});
			}
		}]);

		return ProviderAuth;
	})();

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
				logger.log({ description: 'Signup called.', signupData: signupData, func: 'signup', obj: 'Matter' });
				if (!signupData) {
					logger.error({ description: 'Signup information is required to signup.', func: 'signup', obj: 'Matter' });
					return Promise.reject({ message: 'Login data is required to login.' });
				}
				if (_.isObject(signupData)) {
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
				} else if (_.isString(signupData)) {
					//Handle 3rd Party signups
					var auth = new ProviderAuth({ provider: signupData, app: this });
					return auth.signup(signupData).then(function (res) {
						logger.info({ description: 'Provider signup successful.', provider: signupData, res: res, func: 'signup', obj: 'Matter' });
						return Promise.resolve(res);
					});
				} else {
					logger.error({ description: 'Incorrectly formatted signup information.', signupData: signupData, func: 'signup', obj: 'Matter' });
					return Promise.reject({ message: 'Signup requires an object or a string.' });
				}
			}

			/** Login
    *
    */
		}, {
			key: 'login',
			value: function login(loginData) {
				var _this4 = this;

				if (!loginData) {
					logger.error({ description: 'Username/Email and Password are required to login', func: 'login', obj: 'Matter' });
					return Promise.reject({ message: 'Login data is required to login.' });
				}
				if (_.isObject(loginData)) {
					if (!loginData.password || !loginData.username) {
						return Promise.reject({ message: 'Username/Email and Password are required to login' });
					}
					//Username/Email Login
					return request.put(this.endpoint + '/login', loginData).then(function (response) {
						if (_.has(response, 'data') && _.has(response.data, 'status') && response.data.status == 409) {
							logger.warn({ description: 'Account not found.', response: response, func: 'login', obj: 'Matter' });
							return Promise.reject(response.data);
						} else {
							logger.log({ description: 'Successful login.', response: response, func: 'login', obj: 'Matter' });
							if (_.has(response, 'token')) {
								_this4.token.string = response.token;
							}
							if (_.has(response, 'account')) {
								_this4.storage.setItem(config.tokenUserDataName, response.account);
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
				} else if (_.isString(loginData)) {
					//Provider login
					var auth = new ProviderAuth({ provider: loginData, app: this });
					return auth.login().then(function (res) {
						logger.info({ description: 'Provider login successful.', provider: loginData, res: res, func: 'login', obj: 'Matter' });
						return Promise.resolve(res);
					});
				} else {
					logger.error({ description: 'Incorrectly fomatted login information.', signupData: signupData, func: 'login', obj: 'Matter' });
					return Promise.reject({ message: 'Login requires an object or a string.' });
				}
			}

			/** Logout
    */
		}, {
			key: 'logout',
			value: function logout() {
				var _this5 = this;

				//TODO: Handle logging out of providers
				if (!this.isLoggedIn) {
					logger.warn({ description: 'No logged in account to log out.', func: 'logout', obj: 'Matter' });
					return Promise.reject({ message: 'No logged in account to log out.' });
				}
				return request.put(this.endpoint + '/logout').then(function (response) {
					logger.log({ description: 'Logout successful.', response: response, func: 'logout', obj: 'Matter' });
					_this5.currentUser = null;
					_this5.token['delete']();
					return response;
				})['catch'](function (errRes) {
					logger.error({ description: 'Error requesting log out: ', error: errRes, func: 'logout', obj: 'Matter' });
					_this5.storage.removeItem(config.tokenUserDataName);
					_this5.token['delete']();
					return Promise.reject(errRes);
				});
			}
		}, {
			key: 'getCurrentUser',
			value: function getCurrentUser() {
				var _this6 = this;

				if (this.storage.item(config.tokenUserDataName)) {
					return Promise.resove(this.storage.getItem(config.tokenUserDataName));
				} else {
					if (this.isLoggedIn) {
						return request.get(this.endpoint + '/user').then(function (response) {
							//TODO: Save user information locally
							logger.log({ description: 'Current User Request responded.', responseData: response, func: 'currentUser', obj: 'Matter' });
							_this6.currentUser = response;
							return response;
						})['catch'](function (errRes) {
							if (errRes.status == 401) {
								logger.warn({ description: 'Called for current user without token.', error: errRes, func: 'currentUser', obj: 'Matter' });
								token['delete']();
								return Promise.resolve(null);
							} else {
								logger.error({ description: 'Error requesting current user.', error: errRes, func: 'currentUser', obj: 'Matter' });
								return Promise.reject(errRes);
							}
						});
					} else {
						return Promise.resolve(null);
					}
				}
			}

			/** updateProfile
    */
		}, {
			key: 'updateProfile',
			value: function updateProfile(updateData) {
				var _this7 = this;

				if (!this.isLoggedIn) {
					logger.error({ description: 'No current user profile to update.', func: 'updateProfile', obj: 'Matter' });
					return Promise.reject({ message: 'Must be logged in to update profile.' });
				}
				//Send update request
				logger.warn({ description: 'Calling update endpoint.', endpoint: this.endpoint + '/user/' + this.token.data.username, func: 'updateProfile', obj: 'Matter' });
				return request.put(this.endpoint + '/user/' + this.token.data.username, updateData).then(function (response) {
					logger.log({ description: 'Update profile request responded.', responseData: response, func: 'updateProfile', obj: 'Matter' });
					_this7.currentUser = response;
					return response;
				})['catch'](function (errRes) {
					logger.error({ description: 'Error requesting current user.', error: errRes, func: 'updateProfile', obj: 'Matter' });
					return Promise.reject(errRes);
				});
			}
		}, {
			key: 'changePassword',
			value: function changePassword() {
				var _this8 = this;

				if (!this.isLoggedIn) {
					logger.error({ description: 'No current user profile for which to change password.', func: 'changePassword', obj: 'Matter' });
					return Promise.reject({ message: 'Must be logged in to change password.' });
				}
				//Send update request
				logger.log({ description: 'Calling update endpoint to change password.', endpoint: this.endpoint + '/user/' + this.token.data.username, func: 'changePassword', obj: 'Matter' });
				return request.put(this.endpoint + '/user/' + this.token.data.username, updateData).then(function (response) {
					logger.log({ description: 'Update password request responded.', responseData: response, func: 'changePassword', obj: 'Matter' });
					_this8.currentUser = response;
					return response;
				})['catch'](function (errRes) {
					logger.error({ description: 'Error requesting password change.', error: errRes, func: 'changePassword', obj: 'Matter' });
					return Promise.reject(errRes);
				});
			}
		}, {
			key: 'recoverPassword',
			value: function recoverPassword() {
				var _this9 = this;

				if (!this.isLoggedIn) {
					logger.error({ description: 'No current user for which to recover password.', func: 'recoverPassword', obj: 'Matter' });
					return Promise.reject({ message: 'Must be logged in to recover password.' });
				}
				//Send update request
				logger.log({ description: 'Calling recover password endpoint.', endpoint: this.endpoint + '/user/' + this.token.data.username, func: 'recoverPassword', obj: 'Matter' });
				return request.put(this.endpoint + '/account/' + this.token.data.username + '/recover', updateData).then(function (response) {
					logger.log({ description: 'Recover password request responded.', responseData: response, func: 'recoverPassword', obj: 'Matter' });
					_this9.currentUser = response;
					return response;
				})['catch'](function (errRes) {
					logger.error({ description: 'Error requesting password recovery.', error: errRes, func: 'recoverPassword', obj: 'Matter' });
					return Promise.reject(errRes);
				});
			}

			/* set currentUser
    * @description Sets currently user data
    */
		}, {
			key: 'isInGroup',

			//Check that user is in a single group or in all of a list of groups
			value: function isInGroup(checkGroups) {
				var _this10 = this;

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
								v: _this10.isInGroups(groupsArray)
							};
						} else {
							//Single group
							var groups = _this10.token.data.groups || [];
							logger.log({ description: 'Checking if user is in group.', group: groupName, userGroups: _this10.token.data.groups || [], func: 'isInGroup', obj: 'Matter' });
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
				var _this11 = this;

				//Check if user is in any of the provided groups
				if (checkGroups && _.isArray(checkGroups)) {
					return _.map(checkGroups, function (group) {
						if (_.isString(group)) {
							//Group is string
							return _this11.isInGroup(group);
						} else {
							//Group is object
							return _this11.isInGroup(group.name);
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
					if (typeof window !== 'undefined' && _.has(window, 'location') && window.location.host === serverUrl) {
						serverUrl = '';
						logger.info({ description: 'Host is Server, serverUrl simplified!', url: serverUrl, func: 'endpoint', obj: 'Matter' });
					}
				} else {
					serverUrl = serverUrl + '/apps/' + this.name;
					logger.log({ description: 'Server url set.', url: serverUrl, func: 'endpoint', obj: 'Matter' });
				}
				return serverUrl;
			}
		}, {
			key: 'currentUser',
			set: function set(userData) {
				logger.log({ description: 'Current User set.', user: userData, func: 'currentUser', obj: 'Matter' });
				this.storage.setItem(config.tokenUserDataName, userData);
			},

			/* get currentUser
    * @description Gets currently logged in user or returns null
    */
			get: function get() {
				if (this.storage.getItem(config.tokenUserDataName)) {
					return this.storage.getItem(config.tokenUserDataName);
				} else {
					return null;
				}
			}

			/* Storage
    *
    */
		}, {
			key: 'storage',
			get: function get() {
				return storage;
			}

			/** Token
    */
		}, {
			key: 'token',
			get: function get() {
				return token;
			}
		}, {
			key: 'utils',
			get: function get() {
				return { logger: logger, request: request, storage: storage, dom: domUtil };
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