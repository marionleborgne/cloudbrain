(function () { 
	'use strict';
	angular.module('cloudbrain.account')
	.controller('AccountCtrl', ['$scope', '$log', '$matter', '$rootScope', '$state', function ($scope, $log, $matter, $rootScope, $state){
		$scope.data = {username:null, password:null};
		$scope.login = function(){
			$log.log('Login called', $scope.data);
			$matter.login({
				username:$scope.data.username, 
				password: $scope.data.password
			})
			.then(function (loginRes){
				$log.log('Successful login:', loginRes);
				$rootScope.currentUser = $matter.currentUser;
				$rootScope.$digest();
				$state.go('chart');
			}, function (err){
				$log.error('Error logging in:', err);
			});
		};
		$scope.logout = function(){
			$log.log('Login called', $scope.data);
			$matter.logout()
			.then(function (){
				$log.log('Successful logout');
				$rootScope.currentUser = null;
				$rootScope.$digest();
				$state.go('home');
			}, function (err){
				$log.error('Error logging out:', err);
			});
		};
		$scope.signup = function(){
			$log.log('Login called', $scope.data);
			if(!$scope.data.username || !$scope.data.username){
				$scope.showToast('Username and password are required to signup');
			} else {
				$matter.signup({
					username:$scope.data.username,
					password: $scope.data.password
				})
				.then(function (loginRes){
					$log.log('Successful login:', loginRes);
					$scope.showToast('Logged In');
				}, function (err){
					$log.error('Error logging in:', err);
					var msg = 'Login Error';
					if(err && err.message){
						msg += ' ' + err.message;
					}
					$scope.showToast(msg);
				});
			}
		};
	}]);
})();
