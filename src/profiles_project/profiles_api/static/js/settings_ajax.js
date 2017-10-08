/**
* Función que arma las configuraciones de la petición Ajax a los servicios web.
* data: Datos que se enviarán en el cuarpo de la petición (Array)
* header: Array de headers de la petición, se agrega el permiso de autenticación.
**/
function apiRequest(data, headers, server, service, pk, auth) {

  if (auth)
    headers['Authorization'] = 'token {0}'.format(localStorage.getItem('token'));
  headers['cache-control'] = 'no-cache';

	var settings = {
		"async": true,
    "crossDomain": true,
    "url": server + service.url + pk,
    "method": service.method,
    "headers": headers,
    "processData": false,
    "data": data,
    beforeSend: function () {

    },
    complete: function (response) {

    },
    success: function (response) {
      //console.log(response);
    },
    error: function (response) {
      console.log('Ajax request fail');
      console.log(response);
      // swal("Error!", response.responseText, "error");
    }
	}

	return settings;
}
