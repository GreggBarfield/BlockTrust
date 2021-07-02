$(function() {
    if ("rememberMe" in localStorage && localStorage.rememberMe) {
        $('#remember_me').attr('checked', 'checked');
        $('#login_username').val(localStorage.username);
        $('#login_password').val(localStorage.password);
    } else {
        $('#remember_me').removeAttr('checked');
        $('#login_username').val('');
        $('#login_password').val('');
    }

    $("form").submit(function(){
        if ($('#remember_me').is(':checked')) {
            // save username and password
            localStorage.username = $('#login_username').val();
            localStorage.password = $('#login_password').val();
            localStorage.rememberMe = true;
        }
    });
});