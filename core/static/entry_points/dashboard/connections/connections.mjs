var removeConnectionButtons = document.getElementsByClassName("btn-danger");
for(const el of removeConnectionButtons) {
    // Need to implement remove connection function here in future
}
function accept(current){
  let accountID = {"account_id": current.value};
  let accountIDString = JSON.stringify(accountID);
  fetch(
    "/dashboard/accept-invite",{
      method: "POST",
      body: accountIDString,
      headers: {"Content-type": "application/json; charset=UTF-8"}
    })
    .then(function(response){
      if(response.status == 200){
        location.reload();
      }
    });
}
function decline(current){
  let accountID = {"account_id": current.value};
  let accountIDString = JSON.stringify(accountID);
  fetch(
    "/dashboard/decline-invite",{
      method: "POST",
      body: accountIDString,
      headers: {"Content-type": "application/json; charset=UTF-8"}
    })
    .then(function(response){
      if(response.status == 200){
        location.reload();
      }
    });
}