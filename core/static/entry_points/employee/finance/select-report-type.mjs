$(document).ready(function () {
$(".form-inline").submit(function(event){
    event.preventDefault();
    var type_selected = $(".form-inline").find("#type").val();
    window.location.href = '/employee/dashboard/select-report-type/'+type_selected;
    return false;
});
});