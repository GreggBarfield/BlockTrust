$(document).ready(function () {
    $('#sector').change(function () {
        $('#company_name').empty();
        $('#company_name').append(`<option value="Not Listed">Not Listed</option>`);
        if($(this).val() == 4){
            for(let val in accounts){
                if(accounts[val].name!=="" && accounts[val].company!==null && accounts[val].sector==4){
                    $('#company_name').append(`<option value="${accounts[val].company}">${accounts[val].company}</option>`);
                }
            }
        }
        if($(this).val() == 5){
            for(let val in accounts){
                if(accounts[val].name!=="" && accounts[val].company!==null && accounts[val].sector==5){
                    $('#company_name').append(`<option value="${accounts[val].company}">${accounts[val].company}</option>`);
                }
            }
        }
        if($(this).val() == 6){
            for(let val in accounts){
                if(accounts[val].name!=="" && accounts[val].company!==null && accounts[val].sector==6){
                    $('#company_name').append(`<option value="${accounts[val].company}">${accounts[val].company}</option>`);
                }
            } 
        }
        if($(this).val() == 7){
            for(let val in accounts){
                if(accounts[val].name!=="" && accounts[val].company!==null && accounts[val].sector==7){
                    $('#company_name').append(`<option value="${accounts[val].company}">${accounts[val].company}</option>`);
                }
            } 
        }

    })
})