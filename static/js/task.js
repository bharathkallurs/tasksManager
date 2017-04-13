var tasker = angular.module('taskApp', ['720kb.datepicker', 'ngToast']);

tasker.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{a');
  $interpolateProvider.endSymbol('a}');
}]);

tasker.controller("taskController", function($scope, $http, ngToast){
    $scope.task = {};
    $scope.task_detail = {};
    var start_date;
    var end_date;

    // set today's date to minimum limit
    $scope.minDate = new Date().toString();
    console.log($scope.minDate);

    var ngToastmsg = function(ngToast, contentType, msg){
        ngToast.create({
            className: contentType,
            content: '<a href="#" class="">'.concat(msg, '</a>'),
            dismissButton: true,
            timeout: 4800
        });
    };

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
                        ngToastmsg(ngToast, 'success', response.data.result);
                        $scope.listTasks();
                    }, function(error) {
                        ngToastmsg(ngToast, 'danger', error.data);
                        console.log(error.data);
                    });
    };

    $scope.listTasks = function() {
        $scope.tasks = {};
        $http({
            method: 'GET',
            url: '/task/list'
        }).then(function(response) {
                    $scope.tasks = response.data.result;
                }, function(error) {
                    ngToastmsg(ngToast, 'danger', error.data);
                    console.log(error);
        });
    };

    $scope.listTaskDateRange = function() {
        start_date = $("#listStDt").val();
        end_date = $("#listEnDt").val();
        console.log('start date', start_date);
        console.log('end date', end_date);

        $http({
            method: 'GET',
            url: '/task/list_bw_cr_dt/'.concat(start_date, '/', end_date)
        }).then(function(response) {
            $scope.tasks = response.data.result;
            console.log('list', $scope.tasks);
            $("#listRange").modal('hide');
            //ngToastmsg(ngToast, 'info', response.data.result);
        }, function(error) {
            ngToastmsg(ngToast, 'danger', error.data);
            console.log(error);
        });
    };

    $scope.getTask = function(id){
        $scope.id = id;
        $http({
            method: 'GET',
            url: '/task/get/'.concat(id),

        }).then(function(response) {
                        $scope.task_detail = response.data.result[0];
                        console.log('task_detail', $scope.task_detail);
                    }, function(error) {
                        ngToastmsg(ngToast, 'danger', error.data);
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
                ngToastmsg(ngToast, 'success', response.data.result);
            }, function(error) {
                ngToastmsg(ngToast, 'danger', error.data);
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
            ngToastmsg(ngToast, 'success', response.data.result);
        }, function(error){
            ngToastmsg(ngToast, 'danger', error.data);
            console.log(error);
        });
    };

    // Call this on page load to list all the tasks
    $scope.listTasks();
});
