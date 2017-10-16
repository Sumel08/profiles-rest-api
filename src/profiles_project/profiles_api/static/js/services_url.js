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

var service_patchEvent = {
  'method': 'PATCH',
  'url': 'event/'
}

var service_getChair = {
  'method': 'GET',
  'url': 'chair/'
}

var service_postChair = {
  'method': 'POST',
  'url': 'chair/'
}

var service_getSponsor = {
  'method': 'GET',
  'url': 'sponsor/'
}

var service_postSponsor = {
  'method': 'POST',
  'url': 'sponsor/'
}

var service_getDeveloper = {
  'method': 'GET',
  'url': 'developer/'
}

var service_postDeveloper = {
  'method': 'POST',
  'url': 'developer/'
}

var service_getStream = {
  'method': 'GET',
  'url': 'stream/'
}

var service_postStream = {
  'method': 'POST',
  'url': 'stream/'
}

var service_getSketch = {
  'method': 'GET',
  'url': 'event/sketch'
}

var service_postSketch = {
  'method': 'POST',
  'url': 'sketch/'
}

var service_createImage = {
  'method': 'POST',
  'url': 'image/'
}

var service_getActivity = {
  'method': 'GET',
  'url': 'activity/'
}

var service_postActivity = {
  'method': 'POST',
  'url': 'activity/'
}

var service_getActivityType = {
  'method': 'GET',
  'url': 'activityType/'
}

var service_postActivityPeople = {
  'method': 'POST',
  'url': 'activityPeople/'
}

var service_postActivityType = {
  'method': 'POST',
  'url': 'activityType/'
}

var service_getPlace = {
  'method': 'GET',
  'url': 'place/'
}

var service_createPlace = {
  'method': 'POST',
  'url': 'place/'
}

var service_deletePlace = {
  'method': 'DELETE',
  'url': 'place/'
}

var service_getPlaceCategory = {
  'method': 'GET',
  'url': 'placeCategory/'
}

var service_postPlaceCategory = {
  'method': 'POST',
  'url': 'placeCategory/'
}

var service_deletePlaceCategory = {
  'method': 'DELETE',
  'url': 'placeCategory/'
}

var service_createPeople = {
  'method': 'POST',
  'url': 'people/'
}

var service_getPeople = {
  'method': 'GET',
  'url': 'people/'
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

function getEventName() {
  var data = {};
  var headers = {};

  var settings = apiRequest(data, headers, server_ip, service_myEvent, '', true);

  $.ajax(settings).done(function (response) {
      $('#event_title').html(response.name);
  }).fail(function(jqXHR, textStatus, errorThrown) {
      goPage('create_event');
  });
}
