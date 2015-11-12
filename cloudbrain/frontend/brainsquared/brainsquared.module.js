(function () {
	'use strict';

	angular.module('cloudbrain.brainsquared', ['rt.eventemitter'])
		.constant('MODULE_URL', 'http://brainsquared.apiserver.cloudbrain.rocks/api/v0.1/users/brainsquared/modules')
		// .constant('CREATE_TAG_URL', 'http://localhost:8080/api/v0.1/users/brainsquared/modules/module0/tag')
		.constant('STREAM_MODE', true);
})();
