var form = document.createElement("form");
form.className = "bg-white"
form.id = "select_account_form"

var form_group=document.createElement("div");
form_group.className = "form-group";

var select = document.createElement("select");
select.name = "accounts";
select.id = "accounts"
select.className = "form-control"
for (let val in accounts)
{
    var option = document.createElement("option");
    option.value = accounts[val].id;
    option.text = accounts[val].company;
    select.appendChild(option);
}
form_group.appendChild(select);

var s = document.createElement("input");
s.setAttribute("type", "submit");
s.setAttribute("value", "Submit");
s.setAttribute("class", "btn btn-primary");

form.append(form_group);
form.appendChild(s);

form.onsubmit = function(event){
    event.preventDefault();
    var account_selected = select.value;
    window.location.href = "/employee/dashboard/edit-account/"+ account_selected;
};
document.getElementById("card-body").appendChild(form);
