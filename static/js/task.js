var tasker = angular.module('taskApp', ['720kb.datepicker']);

tasker.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{a');
  $interpolateProvider.endSymbol('a}');
}]);

tasker.controller("taskController", function($scope, $http){
    $scope.task = {};
    $scope.task_detail = {};

    $scope.addTask = function(){
        console.log($scope.task);
        var createCall = $http({
                method: 'POST',
                url: '/task/add',
                data: {
                    task: $scope.task
                }
            });

        $('#createTask').modal('hide');

        createCall.then(function(response) {
                        $scope.task = {};
                        alert(response.data.result);
                        $scope.listTasks();
                    }, function(error) {
                        alert(error.result);
                        console.log(error);
                    });
                };

    $scope.listTasks = function() {
        $http({
            method: 'GET',
            url: '/task/list',

        }).then(function(response) {
                        $scope.tasks = response.data.result;
                    }, function(error) {
                        console.log(error);
                    });
                };

    $scope.listTaskDateRange = function() {
        var start_date = $("#listStDt").val();
        var end_date = $("#listEnDt").val();
        console.log('start date', start_date);
        console.log('end date', end_date);

        $http({
            method: 'GET',
            url: '/task/list_bw_cr_dt/'.concat(start_date, '/', end_date)
        }).then(function(response) {
            $scope.tasks = response.data.result;
            $("#listRange").modal('hide');
        }, function(error) {
            console.log(error);
        });
    };

    // Call this on page load to list all the tasks
    $scope.listTasks();

    $scope.getTask = function(id){
        $scope.id = id;
        $http({
            method: 'GET',
            url: '/task/get/'.concat(id),

        }).then(function(response) {
                        $scope.task_detail = response.data.result[0];
                        console.log('task_detail', $scope.task_detail);
                    }, function(error) {
                        console.log(error);
                    });
                };

    $scope.updateTask = function(){
                    console.log("before");
                    console.log($scope.task_detail);
					var updateCall = $http({
						method: 'PUT',
						url: '/task/update/'.concat($scope.task_detail['task_id']),
						data: {task : $scope.task_detail}
					});

					$('#updateTask').modal('hide');

                    updateCall.then(function(response) {
						console.log(response.data);
						$scope.listTasks();
						alert(response.data.result);
					}, function(error) {
						console.log(error);
					});
				};

    $scope.deleteTask = function(){
                    var deleteCall = $http({
                        method: 'GET',
                        url: '/task/delete/'.concat($scope.task_detail['task_id']),
                    });

                    $("#deleteTask").modal('hide');

                    deleteCall.then(function(response){
                        $scope.listTasks();
                        alert(response.data.result);
                    }, function(error){
                        console.log(error);
                    });
                };
});
