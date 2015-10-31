(function () {
	'use strict';

	angular.module('cloudbrain.brainsquared', ['rt.eventemitter'])
		.constant('CREATE_TAG_URL', 'http://192.168.1.35:8080/api/v0.1/users/brainsquared/modules/debug/tag')
		.constant('STREAM_MODE', false);
		// .constant('CREATE_TAG_URL', 'http://apiserver.cloudbrain.rocks/api/v1.0/users/numenta/tags');
})();
