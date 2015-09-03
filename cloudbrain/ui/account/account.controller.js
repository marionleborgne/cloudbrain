(function () { 
	'use strict';
	angular.module('cloudbrain.account')
	.controller('AccountCtrl', ['$scope', '$log', function ($scope, $log){
		var matter = new Matter('cloudbrain');
		$scope.data = {username:null, password:null};
		$log.log('Matter created:', matter);
		$scope.login = function(){
			$log.log('Login called', $scope.data);
			matter.login({
				username:$scope.data.username, 
				password: $scope.data.password
			})
			.then(function (loginRes){
				$log.log('Successful login:', loginRes);
			}, function (err){
				$log.error('Error logging in:', err);
			});
		};
		$scope.logout = function(){
			$log.log('Login called', $scope.data);
			matter.logout()
			.then(function (){
				$log.log('Successful logout');
			}, function (err){
				$log.error('Error logging out:', err);
			});
		};
		$scope.signup = function(){
			$log.log('Login called', $scope.data);
			matter.signup({
				username:$scope.data.username, 
				password: $scope.data.password
			})
			.then(function (loginRes){
				$log.log('Successful login:', loginRes);
			}, function (err){
				$log.error('Error logging in:', err);
			});
		};
	}]);
})();
