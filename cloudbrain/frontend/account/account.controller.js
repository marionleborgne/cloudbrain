(function () {
	'use strict';
	angular.module('cloudbrain.account')
	.controller('AccountCtrl', ['$scope', '$log', '$matter', '$rootScope', '$state', function ($scope, $log, $matter, $rootScope, $state){
		$scope.data = {username:null, password:null};
		var DEMO_LOGINS = ['will', 'marion', 'amsterdam', 'paris', 'dublin',
											 'montreal', 'nyc', 'sf', 'toronto', 'neurotechx',
										 	 'htmchallenge', 'brainsquared', 'demo1', 'demo2', 'demo3',
											 'demo4', 'demo5', 'demo6', 'demo7', 'demo8', 'demo9', 'demo10'];

		$scope.login = function(){
			$log.log('Login called', $scope.data);
			$scope.data.loading = true;
			if(DEMO_LOGINS.indexOf($scope.data.username) >= 0 && $scope.data.username === $scope.data.password) {
					$log.log('Successful login:', $scope.data.username);
					$scope.data.loading = false;
					$rootScope.currentUser = $matter.currentUser || $scope.data;
					$scope.showToast('Logged In');
					$state.go('rtchart');
			}else{
					$scope.data.loading = false;
					$log.error('Error logging in');
					$scope.showToast('Login Error: Invalid Credentials');
			}
		};
		$scope.logout = function(){
			$log.log('Login called', $scope.data);
			$log.log('Successful logout');
			$rootScope.currentUser = null;
			$scope.showToast('Logged Out');
			$state.go('home');
		};
		$scope.signup = function(){
			$log.log('Signup called', $scope.data);
			if(!$scope.data.username || !$scope.data.username){
				$scope.showToast('Username and password are required to signup');
			} else {
				$scope.showToast('Email us to get access to the alpha demo');
				//
				// $log.log('Successful login:', $scope.data);
				// $rootScope.currentUser = $matter.currentUser || $scope.data;
				// $scope.showToast('Logged In');
				// $state.go('rtchart');
			}
		};
	}]);
})();
