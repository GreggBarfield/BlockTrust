function accept(current){
    var xhttp = new XMLHttpRequest();
    var account_id = {"account_id": current.value}
    var account_id_json = JSON.stringify(account_id);
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        location.reload();
        }
    };
    xhttp.open("POST", "/dashboard/accept-invite", true);
    xhttp.setRequestHeader("Content-type", 'application/json;charset=UTF-8');
    xhttp.send(account_id_json);
}


function decline(current){
    var xhttp = new XMLHttpRequest();
    var account_id = {"account_id": current.value}
    var account_id_json = JSON.stringify(account_id);
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        location.reload();
        }
    };
    xhttp.open("POST", "/dashboard/decline-invite", true);
    xhttp.setRequestHeader("Content-type", 'application/json;charset=UTF-8');
    xhttp.send(account_id_json);
}