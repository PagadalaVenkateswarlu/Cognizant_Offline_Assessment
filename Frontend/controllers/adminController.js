app.controller("adminController", function($scope, apiService){

$scope.slots = [];

function loadUsers(){

apiService.getUsers()

.then(function(response){

$scope.slots = response.data;

});

}

loadUsers();

$scope.cancelSlot = function(slot){

apiService.cancelSlot(slot.user_id, slot.user_id)

.then(function(){

alert("Slot cancelled");

loadUsers();

});

};

});