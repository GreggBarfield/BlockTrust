$(document).ready(function() {
    var startDate=document.getElementById("start_date");
    var daysRemaining = document.getElementById("days_remaining");
    let numberDaysRemaining = "--";

    if (start!==null){
        var date = new Date(start * 1000);
        startDate.textContent = date.toDateString();
    }
    else{
        startDate.textContent = "N/A"
    }
    if (end !== null) {
        let currentEpoch = Date.now() / 1000;
        numberDaysRemaining = Math.floor((end - currentEpoch) / (60 * 60 * 24));
        if(numberDaysRemaining>0){
            daysRemaining.textContent = numberDaysRemaining
        }
        else{
            daysRemaining.textContent = "--"
        }
    }
    else{
        daysRemaining.textContent = "--"
    }
});