function completeOnboardingStatus(user_id){
    var xhttp = new XMLHttpRequest();
    var user_id = {"user_id": user_id}
    var user_id_json = JSON.stringify(user_id);
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        location.reload();
        }
    };
    xhttp.open("POST", "/dashboard/complete-onboarding-status", true);
    xhttp.setRequestHeader("Content-type", 'application/json;charset=UTF-8');
    xhttp.send(user_id_json);
}
$('#add-data').on('hidden.bs.modal', function (e) {
    if(onboarding_status!=2){
        completeOnboardingStatus(user_id);
    }
})

// Remove usage of user_id