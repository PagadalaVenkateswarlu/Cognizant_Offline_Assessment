var app = angular.module("eventApp", ["ngRoute"]);

app.config(function ($routeProvider) {

$routeProvider

.when("/create-slot", {
    templateUrl: "views/create-slot.html",
    controller: "slotController"
})

.when("/book-slot", {
    templateUrl: "views/book-slot.html",
    controller: "bookingController"
})

.when("/admin-users", {
    templateUrl: "views/admin-users.html",
    controller: "adminController"
})

.otherwise({
    redirectTo: "/book-slot"
})

});