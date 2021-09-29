$(document).ready(function () {
    for(let val in accounts){
        if(accounts[val].name!=="" && accounts[val].company!==null){
            $("#account").append(`<option value="${accounts[val].id}">${accounts[val].company}</option>`)
        }
}

$(".form-inline").submit(function(event){
    event.preventDefault();
    var values = $(this).serializeArray();
    var account_selected = values[0].value;
    window.location.href = '/employee/dashboard/view-accounts/'+ account_selected;
    return false;
});
});
