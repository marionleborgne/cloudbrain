/* global angular */
(function () { 'use strict';

  var app = angular.module('cloudbrain')
  app.config(function($stateProvider, $urlRouterProvider) {
  $stateProvider
    .state('home', {
      url:'/',
      templateUrl:'home/home-index.html'
    })
    .state('chart', {
      url:'/chart',
      templateUrl:'chart/chart-index.html',
      controller:'ChartCtrl'
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
    })
    //Protected state
    // .state('app', {
    //   url:'/apps/:name',
    //   authorizedRoles:[USER_ROLES.admin, USER_ROLES.editor, USER_ROLES.user],
    //   templateUrl:'applications/application.html',
    //   controller:'ApplicationCtrl'
    // })
  // if none of the above states are matched, use this as the fallback
  $urlRouterProvider.otherwise('/');
})

})();
