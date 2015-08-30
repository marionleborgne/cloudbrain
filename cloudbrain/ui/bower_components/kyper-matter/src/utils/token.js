import config from '../config';
import storage from './browserStorage';

class token {
	get str() {
		return storage.getItem(config.tokenName);
	}
	str() {
		return storage.setItem(config.tokenName, tokenStr);
	}
	get data() {
		//TODO: Decode token
	}
	save(tokenStr) {
		this.str = tokenStr;
		storage.setItem(config.tokenName, tokenStr);
	}

	delete() {
		storage.removeItem(config.tokenName);
	}
}

export default token;
