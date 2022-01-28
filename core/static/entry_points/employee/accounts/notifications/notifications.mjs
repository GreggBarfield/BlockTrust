function archive(current){ 
  var notification_id = {"notification_id": current.value}
  var notification_id_json = JSON.stringify(notification_id);
  fetch("/employee/dashboard/archive-notification",{
    method: "POST",
    body: notification_id_json,
    headers: {
      "Content-type": "application/json;charset=UTF-8"
    }
  })
  .then(function(r){
    location.reload();
  })
  .catch(function(error){
    alert("Archive failed");
  });
}