$(document).ready(function () {
    for(let val in accounts){
        if(accounts[val].name!=="" && accounts[val].company!==null){
            $("#account").append(`<option value="${accounts[val].id}">${accounts[val].company}</option>`)
        }
}
$("#select_account_form").submit(function(event){
    event.preventDefault();
    var account_selected = $("#select_account_form").find("#account").val();
    window.location.href = "/employee/dashboard/edit-account/"+ account_selected;
    return false;
})
});
