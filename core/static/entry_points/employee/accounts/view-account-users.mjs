$(document).ready(function () {
    for(let val in account_users){
        if(account_users[val].name!=="" && account_users[val].company!==null){
            $("#users").append(`<option value="${account_users[val].id}">${account_users[val].first_name} ${account_users[val].last_name}</option>`)
        }
}
$(".form-inline").submit(function(event){
    event.preventDefault();
    var user_selected = $(".form-inline").find("#users").val();
    window.location.href = '/employee/dashboard/login-as-user/'+ user_selected;
    return false;
});

});
