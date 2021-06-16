$(function() {
    if (localStorage.chkbx && localStorage.chkbx != '') {
        $('#remember_me').attr('checked', 'checked');
        $('#login_username').val(localStorage.usrname);
        $('#login_password').val(localStorage.pass);
    } else {
        $('#remember_me').removeAttr('checked');
        $('#login_username').val('');
        $('#login_password').val('');
    }

    $('#remember_me').click(function() {

        if ($('#remember_me').is(':checked')) {
            // save username and password
            localStorage.usrname = $('#login_username').val();
            localStorage.pass = $('#login_password').val();
            localStorage.chkbx = $('#remember_me').val();
        } else {
            localStorage.usrname = '';
            localStorage.pass = '';
            localStorage.chkbx = '';
        }
    });
});