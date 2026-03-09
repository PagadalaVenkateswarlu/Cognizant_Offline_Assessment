app.controller("slotController", function($scope, apiService){

$scope.slot = {
    start_time:"",
    end_time:"",
    week:1,
    category_id:1,
    is_admin:true
};

$scope.createSlot = function(){

apiService.createSlot($scope.slot)

.then(function(response){

$scope.message = response.data.detail;

})

.catch(function(error){

$scope.error = error.data.detail;

});

};

});