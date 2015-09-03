import config from '../config';
import storage from './browserStorage';

class token {
	get string() {
		return storage.getItem(config.tokenName);
	}
	get data() {
		//TODO: Decode token
	}
	string(tokenStr) {
		console.log('Token was set', tokenStr);
		return storage.setItem(config.tokenName, tokenStr);
	}
	save(tokenStr) {
		this.string = tokenStr;
		storage.setItem(config.tokenName, tokenStr);
	}
	delete() {
		storage.removeItem(config.tokenName);
	}
}

export default token;
