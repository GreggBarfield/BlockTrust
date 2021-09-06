$(".acceptButton").click(function(e){
    var idClicked=e.target.value;
    $.ajax({
        url: "/dashboard/acceptinvite",
        data: JSON.stringify({
            "action": "accept_invite",
            "params": {
                "account_id": idClicked
            }
        }),
        contentType: 'application/json',
        method: "POST"
    })
    .fail((jqXHR, textStatus) => {
        let e = "HTTP error " + jqXHR.status + " " + textStatus + ": " + jqXHR.responseText;
        console.log(e);
    })
    .then(()=>{
        location.reload();
    })
    .always(()=>{
    });
})


$(".declineButton").click(function(e){
    var idClicked=e.target.value;
    $.ajax({
        url: "/dashboard/declineinvite",
        data: JSON.stringify({
            "action": "decline_invite",
            "params": {
                "account_id": idClicked
            }
        }),
        contentType: 'application/json',
        method: "POST"
    })
    .fail((jqXHR, textStatus) => {
        let e = "HTTP error " + jqXHR.status + " " + textStatus + ": " + jqXHR.responseText;
        console.log(e);
    })
    .then(()=>{
        location.reload();
    })
    .always(()=>{
    });
})