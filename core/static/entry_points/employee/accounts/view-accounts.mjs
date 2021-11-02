$(document).ready(function () {
    for(let val in accounts){
        $("#accounts").append(`<option value="${accounts[val].id}">${accounts[val].name}</option>`)
}

$(".form-inline").submit(function(event){
    event.preventDefault();
    var account_selected = $(".form-inline").find("#accounts").val();
    window.location.href = '/employee/dashboard/view-accounts/'+ account_selected;
    return false;
});
});
