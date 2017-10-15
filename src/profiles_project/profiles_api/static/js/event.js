var event_id = 0;

$(document).ready(function() {
  getEventName();
  getEventData();
  getPlaces();
});

function getEventData() {
  var data = {};
  var headers = {};

  var settings = apiRequest(data, headers, server_ip, service_myEvent, '', true);

  $.ajax(settings).done(function (response) {
      event_id = response.id;
      $('#event_name').html(response.name);
      $('#event_code').html(response.code);
      $('#event_date').html('<i class="material-icons">access_time</i> {0}'.format(response.event_date));
      $('#event_image').attr('src', response.event_image_url);
      if (response.place) {
        console.log('Hay lugar de evento');
        console.log(response.place);
        getPlaceEvent(response.place);
      } else {
        console.log('No hay lugar de evento');
      }
  }).fail(function(jqXHR, textStatus, errorThrown) {

  });
}

function getPlaceEvent(place_id) {
  var settings = apiRequest([], [], server_ip, service_getPlace, place_id, true);

  $.ajax(settings).done(function (response) {

      console.log(response);
      $('#place_image').attr('src', response.image_url);
      $('#place_name').html(response.name);
      $('#place_description').html(response.description);
  });
}

function getPlaces() {
  var settings = apiRequest([], [], server_ip, service_getPlace, '', true);

  $.ajax(settings).done(function (response) {

      $("#select_changePlace").empty();
      $("#select_changePlace").append('<option disabled selected>Select a plce</option>');
      $.each(response, function(index, value) {
        $("#select_changePlace").append('<option value={0}>{1}</option>'.format(value.id, value.name));
      });
      $("#select_changePlace").selectpicker('refresh');
  });
}

function changePlace() {
  if ($('#create_changePlace_form').valid()) {
    console.log('Valid');

    var form = new FormData();
    form.append("place", $('#select_changePlace').val());

    var headers = {
      "cache-control": "no-cache"
    }

    var settings = apiRequest(form, headers, server_ip, service_patchEvent, event_id + '/', true);

    settings['contentType'] = false;
    settings['mimeType'] = 'multipart/form-data';

    $.ajax(settings).done(function (response) {
        console.log('Cambio correcto');
        $('#change_place').modal('hide');
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.log('Falla cambio');
    });
  } else {
    console.log('No valid');
  }
}
