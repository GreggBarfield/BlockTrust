
document.addEventListener("DOMContentLoaded", function(event) {
    
    let accountsDropDown = document.getElementById("accounts");

    for(let val in accounts){    
        var option = document.createElement("option");
        option.value = accounts[val].id;
        option.textContent = accounts[val].company;
        accountsDropDown.appendChild(option);
    }

    const form = document.getElementById('select_account_form');
    form.addEventListener('submit', function(event){
        event.preventDefault();
        window.location.href = "/employee/dashboard/edit-account/"+ accountsDropDown.value;
    });
});