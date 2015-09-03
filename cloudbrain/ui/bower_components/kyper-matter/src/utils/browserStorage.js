import config from '../config';

let storage = {
	get exists() {
		const testKey = 'test';
		if (typeof window != 'undefined') {
			try {
				window.sessionStorage.setItem(testKey, '1');
				window.sessionStorage.removeItem(testKey);
				return true;
			} catch (err) {
				console.warn('Session storage does not exist.', err);
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
	 *  @private
	 */
	setItem(itemName, itemValue) {
		//TODO: Handle itemValue being an object instead of a string
		if (this.exists) {
			window.sessionStorage.setItem(itemName, itemValue);
		}
	},
	/**
	 * @description
	 * Safley gets an item from session storage.
	 *
	 * @param {String} itemName The items name
	 *
	 * @return {String}
	 *
	 */
	getItem(itemName) {
		if (this.exists) {
			return window.sessionStorage.getItem(itemName);
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
		if (this.exists) {
			try {
				//Clear session storage
				window.sessionStorage.removeItem(itemName);
			} catch (err) {
				console.warn('Item could not be removed from session storage.', err);
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
	 *  @private
	 */
	clear() {
		//TODO: Only remove used items
		if (this.exists) {
			try {
					//Clear session storage
				window.sessionStorage.clear();
			} catch (err) {
				console.warn('Session storage could not be cleared.', err);
			}
		}
	}

};

export default storage;

