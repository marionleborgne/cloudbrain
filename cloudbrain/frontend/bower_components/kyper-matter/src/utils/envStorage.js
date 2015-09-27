import config from '../config';
import logger from './logger';
import _ from 'lodash';

let data = {};
let storage = {
	get localExists() {
		const testKey = 'test';
		if (typeof window != 'undefined' && typeof window.sessionStorage != 'undefined') {
			try {
				window.sessionStorage.setItem(testKey, '1');
				window.sessionStorage.removeItem(testKey);
				return true;
			} catch (err) {
				logger.error({description: 'Error saving to session storage', error: err,  obj: 'storage', func: 'localExists'});
				return false;
			}
		} else {
			return false;
		}
	},
	/**
	 * @description
	 * Safley sets item to session storage.
	 *
	 * @param {String} itemName The items name
	 * @param {String} itemValue The items value
	 *
	 */
	item(itemName, itemValue) {
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
	setItem(itemName, itemValue) {
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
	getItem(itemName) {
		if (data[itemName]) {
			return data[itemName];
		} else if (this.localExists) {
			let itemStr = window.sessionStorage.getItem(itemName);
			//Check that str is not null before parsing
			if (itemStr) {
				let isObj = false;
				let itemObj = null;
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
	removeItem(itemName) {
		//TODO: Only remove used items
		if (data[itemName]) {
			data[itemName] = null;
		}
		if (this.localExists) {
			try {
				//Clear session storage
				window.sessionStorage.removeItem(itemName);
			} catch (err) {
				logger.error({description: 'Error removing item from session storage', error: err,  obj: 'storage', func: 'removeItem'});
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
	clear() {
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

};

export default storage;

