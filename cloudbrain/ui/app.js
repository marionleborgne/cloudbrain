/* global angular */
(function () { 'use strict';

  var app = angular.module('cloudbrain', ['ui.bootstrap', 'highcharts-ng', 'cloudbrain.chart'])
  app.value('API_URL', 'http://demo.apiserver.cloudbrain.rocks');

})();
