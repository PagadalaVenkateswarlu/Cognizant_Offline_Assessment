app.service("apiService", function($http){

const BASE_URL = "http://localhost:8000";

this.createSlot = function(slot){
    return $http.post(BASE_URL + "/slots/create", slot);
};

this.bookSlot = function(user, category, week){
    return $http.post(BASE_URL + "/booking-flow?category_id=" + category + "&week=" + week, user);
};

this.getUsers = function(){
    return $http.get(BASE_URL + "/admin/users");
};

this.cancelSlot = function(slot_id, user_id){
    return $http.post(BASE_URL + "/slots/" + slot_id + "/cancel?user_id=" + user_id);
};

});