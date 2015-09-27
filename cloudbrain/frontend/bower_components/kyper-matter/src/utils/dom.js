import logger from './logger';
import _ from 'lodash';

let domUtil = {
	/**
	 * @description
	 * Appends given css source to DOM head.
	 *
	 * @param {String} src - url src for css to append
	 *
	 */
	loadCss: (src) => {
		if (typeof document == 'undefined') {
			logger.error({description: 'Document does not exsist to load assets into.', func: 'loadCss', obj: 'dom'});
			throw new Error('Document object is required to load assets.');
		} else {
			let css = document.createElement('link');
			css.rel = 'stylesheet';
			css.type = 'text/css';
			css.href = src;
			document.getElementsByTagName('head')[0].insertBefore(css, document.getElementsByTagName('head')[0].firstChild);
			logger.log({description: 'CSS was loaded into document.', element: css, func: 'loadCss', obj: 'dom'});
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
	loadJs: (src) => {
		if (typeof window == 'undefined' || !_.has(window, 'document')) {
			logger.error({description: 'Document does not exsist to load assets into.', func: 'loadCss', obj: 'dom'});
			throw new Error('Document object is required to load assets.');
		} else {
			let js = window.document.createElement('script');
			js.src = src;
			js.type = 'text/javascript';
			window.document.getElementsByTagName('head')[0].appendChild(js);
			logger.log({description: 'JS was loaded into document.', element: js, func: 'loadCss', obj: 'dom'});
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
	asyncLoadJs: (src) => {
		if (typeof window == 'undefined' || !_.has(window, 'document')) {
			logger.error({description: 'Document does not exsist to load assets into.', func: 'loadCss', obj: 'dom'});
			throw new Error('Document object is required to load assets.');
		} else {
			let js = window.document.createElement('script');
			js.src = src;
			js.type = 'text/javascript';
			window.document.getElementsByTagName('head')[0].appendChild(js);
			logger.log({description: 'JS was loaded into document.', element: js, func: 'loadCss', obj: 'dom'});
			return new Promise((resolve, reject) => {
				window.setTimeout(resolve, 30);
			});
		}
	}
};
export default domUtil;
