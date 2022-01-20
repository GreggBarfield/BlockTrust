$("#notification_type_button").click(function(){
    var notification_type = document.getElementById("notification_type");
    if(notification_type.value!=""){
        window.location.href = "/employee/dashboard/create-new-notification/"+notification_type.value;
    }
})