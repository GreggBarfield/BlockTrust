function archive(current){
    var xhttp = new XMLHttpRequest();
    var notification_id = {"notification_id": current.value}
    var notification_id_json = JSON.stringify(notification_id);
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        location.reload();
        }
    };
    xhttp.open("POST", "/employee/dashboard/archive-notification", true);
    xhttp.setRequestHeader("Content-type", 'application/json;charset=UTF-8');
    xhttp.send(notification_id_json);
}