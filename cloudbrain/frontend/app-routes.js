/* global angular */
(function () { 'use strict';

  var app = angular.module('cloudbrain')
  app.config(function($stateProvider, $urlRouterProvider) {
  $stateProvider
    .state('home', {
      url:'/',
      templateUrl:'home/home-index.html',
      controller:'HomeCtrl'
    })
    .state('chart', {
      url:'/chart/:device',
      templateUrl:'chart/chart-index.html',
      controller:'ChartCtrl'
    })
    .state('rtchart', {
      url:'/rt-chart/:device',
      template:'<rt-chart></rt-chart>'
    })
    .state('calibration', {
      url:'/calibration',
      template:'<calibration></calibration>'
    })
    .state('brainsquared', {
      url:'/brainsquared',
      template:'<brainsquared></brainsquared>'
    })
    .state('signup', {
      url:'/signup',
      templateUrl:'account/account-signup.html',
      controller:'AccountCtrl'
    })
    .state('login', {
      url:'/login',
      templateUrl:'account/account-login.html',
      controller:'AccountCtrl'
    })
    .state('dashboard', {
      url:'/dash',
      templateUrl:'home/home-index.html'
    });
    //Protected state
    // .state('app', {
    //   url:'/apps/:name',
    //   authorizedRoles:[USER_ROLES.admin, USER_ROLES.editor, USER_ROLES.user],
    //   templateUrl:'applications/application.html',
    //   controller:'ApplicationCtrl'
    // })
  // if none of the above states are matched, use this as the fallback
  $urlRouterProvider.otherwise('/');
});

})();
