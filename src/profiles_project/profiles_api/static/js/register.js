function request_register() {

  if ($('#register_form').valid()) {

    var name = $('#name').val();
    var email = $('#email').val();
    var password = $('#password').val();

    var data = '{"name": "{0}","email": "{1}","password": "{2}"}'.format(name, email, password);

    var headers = {};
    headers['Content-Type'] = 'application/json';

    var settings = apiRequest(data, headers, server_ip, service_register, '');

    $.ajax(settings).done(function (response) {
        console.log(response);
        goPage('login');
    });
  }
}
