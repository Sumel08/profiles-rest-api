var service_login = {
  'method': 'POST',
  'url': 'login/'
}

var service_register = {
  'method': 'POST',
  'url': 'profile/'
}

var service_myEvent = {
  'method': 'GET',
  'url': 'profile/event'
}

var service_createEvent = {
  'method': 'POST',
  'url': 'event/'
}

var service_createImage = {
  'method': 'POST',
  'url': 'image/'
}

function saveImage(file, callback) {
  var form = new FormData();
  form.append("image", file);

  var headers = {
    "cache-control": "no-cache"
  }

  var settings = apiRequest(form, headers, server_ip, service_createImage, '', true);

  settings['contentType'] = false;
  settings['mimeType'] = 'multipart/form-data';

  $.ajax(settings).done(function (response) {
    return callback(jQuery.parseJSON(response));
  }).fail(function (response) {
    console.log('Error subiendo imagen');
    console.log(response);
  });
}
