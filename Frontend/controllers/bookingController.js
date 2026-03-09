app.controller("bookingController", function($scope, apiService){

$scope.user = {
email:"",
username:"",
user_id:"",
is_booked:false
};

$scope.category_id = 1;
$scope.week = 1;

$scope.bookSlot = function(){

apiService.bookSlot($scope.user, $scope.category_id, $scope.week)

.then(function(response){

$scope.message = response.data.message;

})

.catch(function(error){

$scope.error = error.data.detail;

});

};

});