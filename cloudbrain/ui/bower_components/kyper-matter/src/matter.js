import config from './config';
import logger from './utils/logger';
import dom from './utils/dom';
import request from './utils/request';
import token from './utils/token';
import envStorage from './utils/envStorage';
import _ from 'lodash';
import ProviderAuth from './utils/providerAuth';

class Matter {
	/* Constructor
	 * @param {string} appName Name of application
	 */
	constructor(appName, opts) {
		if (!appName) {
			logger.error({description: 'Application name requires to use Matter.', func: 'constructor', obj: 'Matter'});
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
	get endpoint() {
		let serverUrl = config.serverUrl;
		if (_.has(this, 'options') && this.options.localServer) {
			serverUrl = 'http://localhost:4000';
			logger.info({description: 'LocalServer option was set to true. Now server url is local server.', url: serverUrl, func: 'endpoint', obj: 'Matter'});
		}
		if (this.name == 'tessellate') {
			//Remove url if host is server
			if (typeof window !== 'undefined' && _.has(window, 'location') && window.location.host === serverUrl) {
				serverUrl = '';
				logger.info({description: 'Host is Server, serverUrl simplified!', url: serverUrl, func: 'endpoint', obj: 'Matter'});
			}
		} else {
			serverUrl = serverUrl + '/apps/' + this.name;
			logger.log({description: 'Server url set.', url: serverUrl, func: 'endpoint', obj: 'Matter'});
		}
		return serverUrl;
	}
	/* Signup
	 *
	 */
	signup(signupData) {
		logger.log({description: 'Signup called.', signupData: signupData, func: 'signup', obj: 'Matter'});
		if (!signupData || (!_.isObject(signupData) && !_.isString(signupData))) {
			logger.error({description: 'Signup information is required to signup.', func: 'signup', obj: 'Matter'});
			return Promise.reject({message: 'Login data is required to login.'});
		}
		if (_.isObject(signupData)) {
			return request.post(this.endpoint + '/signup', signupData)
			.then((response) => {
				logger.log({description: 'Account request successful.', signupData: signupData, response: response, func: 'signup', obj: 'Matter'});
				if (_.has(response, 'account')) {
					return response.account;
				} else {
					logger.warn({description: 'Account was not contained in signup response.', signupData: signupData, response: response, func: 'signup', obj: 'Matter'});
					return response;
				}
			})
			['catch']((errRes) => {
				logger.error({description: 'Error requesting signup.', signupData: signupData, error: errRes, func: 'signup', obj: 'Matter'});
				return Promise.reject(errRes);
			});
		} else {
			//Handle 3rd Party signups
			let auth = new ProviderAuth({provider: signupData, app: this});
			return auth.signup(signupData).then((res) => {
				logger.info({description: 'Provider signup successful.', provider: signupData, res: res, func: 'signup', obj: 'Matter'});
				return Promise.resolve(res);
			});
		}
	}
	/** Login
	 *
	 */
	login(loginData) {
		if (!loginData || (!_.isObject(loginData) && !_.isString(loginData))) {
			logger.error({description: 'Username/Email and Password are required to login', func: 'login', obj: 'Matter'});
			return Promise.reject({message: 'Login data is required to login.'});
		}
		if (_.isObject(loginData)) {
			if (!loginData.password || !loginData.username) {
				return Promise.reject({message: 'Username/Email and Password are required to login'});
			}
			//Username/Email Login
			return request.put(this.endpoint + '/login', loginData)
			.then((response) => {
				if (_.has(response, 'data') && _.has(response.data, 'status') && response.data.status == 409) {
					logger.warn({description: 'Account not found.', response: response, func: 'login', obj: 'Matter'});
					return Promise.reject(response.data);
				} else {
					logger.log({description: 'Successful login.', response: response, func: 'login', obj: 'Matter'});
					if (_.has(response, 'token')) {
						this.token.string = response.token;
					}
					if (_.has(response, 'account')) {
						this.storage.setItem(config.tokenUserDataName, response.account);
					}
					return response.account;
				}
			})['catch']((errRes) => {
				logger.error({description: 'Error requesting login.', error: errRes, status: errRes.status,  func: 'login', obj: 'Matter'});
				if (errRes.status == 409 || errRes.status == 400) {
					errRes = errRes.response.text;
				}
				return Promise.reject(errRes);
			});
		} else {
			//Provider login
			let auth = new ProviderAuth({provider: loginData, app: this});
			return auth.login().then((res) => {
				logger.info({description: 'Provider login successful.', provider: loginData, res: res, func: 'login', obj: 'Matter'});
				return Promise.resolve(res);
			});
		}
	}
	/** Logout
	 */
	logout() {
		//TODO: Handle logging out of providers
		if (!this.isLoggedIn) {
			logger.warn({description: 'No logged in account to log out.', func: 'logout', obj: 'Matter'});
			return Promise.reject({message: 'No logged in account to log out.'});
		}
		return request.put(this.endpoint + '/logout').then((response) => {
			logger.log({description: 'Logout successful.', response: response, func: 'logout', obj: 'Matter'});
			this.currentUser = null;
			this.token.delete();
			return response;
		})['catch']((errRes) => {
			logger.error({description: 'Error requesting log out: ', error: errRes, func: 'logout', obj: 'Matter'});
			this.storage.removeItem(config.tokenUserDataName);
			this.token.delete();
			return Promise.reject(errRes);
		});
	}
	getCurrentUser() {
		if (this.currentUser) {
			return Promise.resolve(this.currentUser);
		} else {
			if (this.isLoggedIn) {
				return request.get(this.endpoint + '/user').then((response) => {
					//TODO: Save user information locally
					logger.log({description: 'Current User Request responded.', responseData: response, func: 'currentUser', obj: 'Matter'});
					this.currentUser = response;
					return response;
				})['catch']((errRes) => {
					if (errRes.status == 401) {
						logger.warn({description: 'Called for current user without token.', error: errRes, func: 'currentUser', obj: 'Matter'});
						token.delete();
						return Promise.resolve(null);
					} else {
						logger.error({description: 'Error requesting current user.', error: errRes, func: 'currentUser', obj: 'Matter'});
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
	updateProfile(updateData) {
		if (!this.isLoggedIn) {
			logger.error({description: 'No current user profile to update.', func: 'updateProfile', obj: 'Matter'});
			return Promise.reject({message: 'Must be logged in to update profile.'});
		}
		//Send update request
		logger.warn({description: 'Calling update endpoint.', endpoint: `${this.endpoint}/user/${this.token.data.username}` , func: 'updateProfile', obj: 'Matter'});
		return request.put(`${this.endpoint}/user/${this.token.data.username}` , updateData).then((response) => {
			logger.log({description: 'Update profile request responded.', responseData: response, func: 'updateProfile', obj: 'Matter'});
			this.currentUser = response;
			return response;
		})['catch']((errRes) => {
			logger.error({description: 'Error requesting current user.', error: errRes, func: 'updateProfile', obj: 'Matter'});
			return Promise.reject(errRes);
		});
	}
	changePassword(updateData) {
		if (!this.isLoggedIn) {
			logger.error({description: 'No current user profile for which to change password.', func: 'changePassword', obj: 'Matter'});
			return Promise.reject({message: 'Must be logged in to change password.'});
		}
		//Send update request
		logger.log({description: 'Calling update endpoint to change password.', endpoint: `${this.endpoint}/user/${this.token.data.username}` , func: 'changePassword', obj: 'Matter'});
		return request.put(`${this.endpoint}/user/${this.token.data.username}` , updateData).then((response) => {
			logger.log({description: 'Update password request responded.', responseData: response, func: 'changePassword', obj: 'Matter'});
			return response;
		})['catch']((errRes) => {
			logger.error({description: 'Error requesting password change.', error: errRes, func: 'changePassword', obj: 'Matter'});
			return Promise.reject(errRes);
		});
	}
	recoverPassword() {
		if (!this.isLoggedIn) {
			logger.error({description: 'No current user for which to recover password.', func: 'recoverPassword', obj: 'Matter'});
			return Promise.reject({message: 'Must be logged in to recover password.'});
		}
		//Send update request
		logger.log({description: 'Calling recover password endpoint.', endpoint: `${this.endpoint}/accounts/${this.token.data.username}/recover` , func: 'recoverPassword', obj: 'Matter'});
		return request.post(`${this.endpoint}/accounts/${this.token.data.username}/recover`).then((response) => {
			logger.log({description: 'Recover password request responded.', responseData: response, func: 'recoverPassword', obj: 'Matter'});
			return response;
		})['catch']((errRes) => {
			logger.error({description: 'Error requesting password recovery.', error: errRes, func: 'recoverPassword', obj: 'Matter'});
			return Promise.reject(errRes);
		});
	}

	/* set currentUser
	 * @description Sets currently user data
	 */
	set currentUser(userData) {
		logger.log({description: 'Current User set.', user: userData, func: 'currentUser', obj: 'Matter'});
		this.storage.setItem(config.tokenUserDataName, userData);
	}
	/* get currentUser
	 * @description Gets currently logged in user or returns null
	 */
	get currentUser() {
		if (this.storage.getItem(config.tokenUserDataName)) {
			return this.storage.getItem(config.tokenUserDataName);
		} else {
			return null;
		}
	}
	/* Storage
	 *
	 */
	get storage() {
		return envStorage;
	}
	/** Token
	 */
	get token() {
		return token;
	}
	get utils() {
		return {logger: logger, request: request, storage: envStorage, dom: dom};
	}
	get isLoggedIn() {
		return this.token.string ? true : false;
	}
	//Check that user is in a single group or in all of a list of groups
	isInGroup(checkGroups) {
		if (!this.isLoggedIn) {
			logger.log({description: 'No logged in user to check.', func: 'isInGroup', obj: 'Matter'});
			return false;
		}
		//Check if user is
		if (checkGroups && _.isString(checkGroups)) {
			let groupName = checkGroups;
			//Single role or string list of roles
			let groupsArray = groupName.split(',');
			if (groupsArray.length > 1) {
				//String list of groupts
				logger.info({description: 'String list of groups.', list: groupsArray, func: 'isInGroup', obj: 'Matter'});
				return this.isInGroups(groupsArray);
			} else {
				//Single group
				let groups = this.token.data.groups || [];
				logger.log({description: 'Checking if user is in group.', group: groupName, userGroups: this.token.data.groups || [],  func: 'isInGroup', obj: 'Matter'});
				return _.any(groups, (group) =>  {
					return groupName == group.name;
				});
			}
		} else if (checkGroups && _.isArray(checkGroups)) {
			//Array of roles
			//Check that user is in every group
			logger.info({description: 'Array of groups.', list: checkGroups, func: 'isInGroup', obj: 'Matter'});
			return this.isInGroups(checkGroups);
		} else {
			return false;
		}
		//TODO: Handle string and array inputs
	}
	isInGroups(checkGroups) {
		if (!this.isLoggedIn) {
			logger.log({description: 'No logged in user to check.', func: 'isInGroups', obj: 'Matter'});
			return false;
		}
		//Check if user is in any of the provided groups
		if (checkGroups && _.isArray(checkGroups)) {
			return _.every(_.map(checkGroups, (group) =>  {
				if (_.isString(group)) {
					//Group is string
					return this.isInGroup(group);
				} else {
					//Group is object
					if (_.has(group, 'name')) {
						return this.isInGroup(group.name);
					} else {
						logger.error({description: 'Invalid group object.', group: group, func: 'isInGroups', obj: 'Matter'});
						return false;
					}
				}
			}), true);
		} else if (checkGroups && _.isString(checkGroups)) {
			//TODO: Handle spaces within string list
			let groupsArray = checkGroups.split(',');
			if (groupsArray.length > 1) {
				return this.isInGroups(groupsArray);
			}
			return this.isInGroup(groupsArray[0]);
		} else {
			logger.error({description: 'Invalid groups list.', func: 'isInGroups', obj: 'Matter'});
			return false;
		}
	}
};
export default Matter;
