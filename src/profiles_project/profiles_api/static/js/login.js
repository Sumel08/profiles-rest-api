$(document).ready(function() {
  console.log(localStorage.getItem('token'));
});

function request_login() {
  var csrftoken = getCookie('csrftoken');

  if ($('#login_form').valid()) {

    var email = $('#email').val();
    var password = $('#password').val();

    var data = '{"username": "{0}","password": "{1}"}'.format(email, password);

    var headers = {}
    headers['X-CSRFToken'] = csrftoken;
    headers['Content-Type'] = 'application/json';

    var settings = apiRequest(data, headers, server_ip, service_login, '');

    $.ajax(settings).done(function (response) {
        localStorage.setItem('token', response.token);
        goPage('dashboard');
    }).fail(function (response) {
      swal('Error', 'Something went wrong', 'error');
    });
  }
}
