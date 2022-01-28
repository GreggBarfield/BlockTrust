var notification_type_button = document.getElementById("notification_type_button");
notification_type_button.onclick = ()=>{
    var type_selected = document.getElementById("notification_type");
    if(type_selected.value!=""){
        window.location.href = "/employee/dashboard/create-new-notification/"+type_selected.value;
    }
}