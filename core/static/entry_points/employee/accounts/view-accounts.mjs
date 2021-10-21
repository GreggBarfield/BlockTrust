$(document).ready(function () {
    for(let val in accounts){
        if(accounts[val].name!=="" && accounts[val].company!==null){
            $("#accounts").append(`<option value="${accounts[val].id}">${accounts[val].company}</option>`)
        }
}

$(".form-inline").submit(function(event){
    event.preventDefault();
    var account_selected = $(".form-inline").find("#accounts").val();
    window.location.href = '/employee/dashboard/view-accounts/'+ account_selected;
    return false;
});
});
