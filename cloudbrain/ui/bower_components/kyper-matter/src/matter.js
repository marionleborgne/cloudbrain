import config from './config';
import logger from './utils/logger';
import request from './utils/request';
import token from './utils/token';
import envStorage from './utils/envStorage';
import _ from 'lodash';

let user;
let endpoints;

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
			if (window && _.has(window, 'location') && window.location.host == serverUrl) {
				serverUrl = '';
				logger.info({description: 'Host is Server, serverUrl simplified!', url: serverUrl, func: 'endpoint', obj: 'Matter'});
			}
		} else {
			serverUrl = config.serverUrl + '/apps/' + this.name;
			logger.info({description: 'Server url set.', url: serverUrl, func: 'endpoint', obj: 'Matter'});
		}
		return serverUrl;
	}
	/* Signup
	 *
	 */
	signup(signupData) {
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
	}
	/** Login
	 *
	 */
	login(loginData) {
		if (!loginData || !loginData.password || !loginData.username) {
			logger.error({description: 'Username/Email and Password are required to login', func: 'login', obj: 'Matter'});
			return Promise.reject({message: 'Username/Email and Password are required to login'});
		}
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
					this.storage.setItem('currentUser', response.account);
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
	}
	/** Logout
	 */
	logout() {
		return request.put(this.endpoint + '/logout').then((response) => {
			logger.log({description: 'Logout successful.', response: response, func: 'logout', obj: 'Matter'});
			this.storage.removeItem('currentUser');
			this.token.delete();
			return response;
		})['catch']((errRes) => {
			logger.error({description: 'Error requesting log out: ', error: errRes, func: 'logout', obj: 'Matter'});
			this.storage.removeItem('currentUser');
			this.token.delete();
			return Promise.reject(errRes);
		});
	}
	getCurrentUser() {
		if (this.storage.item('currentUser')) {
			return Promise.resove(this.storage.item('currentUser'));
		} else {
			return request.get(this.endpoint + '/user').then((response) => {
				//TODO: Save user information locally
				logger.log({description: 'Current User Request responded.', responseData: response.data, func: 'currentUser', obj: 'Matter'});
				this.currentUser = response.data;
				return response.data;
			})['catch']((errRes) => {
				logger.error({description: 'Error requesting current user.', error: errRes, func: 'currentUser', obj: 'Matter'});
				return Promise.reject(errRes);
			});
		}
	}
	set currentUser(userData) {
		logger.log({description: 'Current User Request responded.', user: userData, func: 'currentUser', obj: 'Matter'});
		this.storage.setItem(userData);
	}
	get currentUser() {
		if (this.storage.getItem('currentUser')) {
			return this.storage.getItem('currentUser');
		} else {
			return null;
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
	/** updateProfile
	 */
	get storage() {
		return envStorage;
	}
	/** updateProfile
	 */
	get token() {
		return token;
	}
	get utils() {
		return {logger: logger, request: request, storage: envStorage};
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
		//Check if user is in any of the provided groups
		if (checkGroups && _.isArray(checkGroups)) {
			return _.map(checkGroups, (group) =>  {
				if (_.isString(group)) {
					//Group is string
					return this.isInGroup(group);
				} else {
					//Group is object
					return this.isInGroup(group.name);
				}
			});
		} else if (checkGroups && _.isString(checkGroups)) {
			//TODO: Handle spaces within string list
			let groupsArray = checkGroups.split(',');
			if (groupsArray.length > 1) {
				return this.isInGroups(groupsArray);
			}
			return this.isInGroup(groupsArray[0]);
		} else {
			logger.error({description: 'Invalid groups list.', func: 'isInGroups', obj: 'Matter'});
		}
	}
};
export default Matter;
