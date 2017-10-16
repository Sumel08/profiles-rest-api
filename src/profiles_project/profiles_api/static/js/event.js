var event_id = 0;

$(document).ready(function() {
  getEventName();
  getEventData();
  getPlaces();
  getChairs();
  getPeople();
  getSponsors();
  getDevelopers();
  getStreams();
  getSketch();
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

function getChairs() {
  var settings = apiRequest([], [], server_ip, service_getChair, '', true);

  $.ajax(settings).done(function (response) {
      $('#chairs').find('table>tbody').empty();
      $.each(response, function(index, value) {
        $('#chairs').find('table>tbody').append(chair_row(value.person_data));
      });
  });
}

function chair_row(element) {
  var row_element = '<tr>' +
                      '<td><img src="{0}" class="img-responsive" style="max-width: 50px;"/></td>'.format(element.photo_url) +
                      '<td>{0} {1}</td>'.format(element.name, element.surname) +
                      '<td>{0}</td>'.format(element.email) +
                      '<td>{0}</td>'.format(element.phone) +
                      '<td class="td-actions text-right">' +
                        '<button type="button" rel="tooltip" title="Edit" class="btn btn-primary btn-simple btn-xs" onclick="editPlace({0})">'.format(element.id) +
                          '<i class="material-icons">edit</i>' +
                        '</button>' +
                        '<button type="button" rel="tooltip" title="Remove" class="btn btn-danger btn-simple btn-xs" onclick="deletePlace({0})">'.format(element.id) +
                          '<i class="material-icons">close</i>' +
                        '</button>' +
                      '</td>' +
                    '</tr>';
  return row_element;
}

function changeChairs() {
  if ($('#create_changeChairs_form').valid()) {
    var chairs = $('#select_changeChairs').val();

    var form = new FormData();

    $.each(chairs, function(index, chair) {
      form.append("people", chair);
    });

    var headers = {
      "cache-control": "no-cache"
    }

    var settings = apiRequest(form, headers, server_ip, service_postChair, '', true);

    settings['contentType'] = false;
    settings['mimeType'] = 'multipart/form-data';

    $.ajax(settings).done(function (response) {
      console.log('Se crea chairs correctamente');
      console.log(response);
      getChairs();
      $('#create_changeChairs_form').trigger('reset');
      $('#selectChairs').modal('hide');
    }).fail(function (response) {
      console.log('No se crea correctamente el place');
      console.log(response);
    });
  }
}

function getSponsors() {
  var settings = apiRequest([], [], server_ip, service_getSponsor, '', true);

  $.ajax(settings).done(function (response) {
      $('#sponsors').find('table>tbody').empty();
      $.each(response, function(index, value) {
        $('#sponsors').find('table>tbody').append(sponsor_row(value.person_data));
      });
  });
}

function sponsor_row(element) {
  var row_element = '<tr>' +
                      '<td><img src="{0}" class="img-responsive" style="max-width: 50px;"/></td>'.format(element.photo_url) +
                      '<td>{0} {1}</td>'.format(element.name, element.surname) +
                      '<td>{0}</td>'.format(element.email) +
                      '<td>{0}</td>'.format(element.phone) +
                      '<td class="td-actions text-right">' +
                        '<button type="button" rel="tooltip" title="Edit" class="btn btn-primary btn-simple btn-xs" onclick="editPlace({0})">'.format(element.id) +
                          '<i class="material-icons">edit</i>' +
                        '</button>' +
                        '<button type="button" rel="tooltip" title="Remove" class="btn btn-danger btn-simple btn-xs" onclick="deletePlace({0})">'.format(element.id) +
                          '<i class="material-icons">close</i>' +
                        '</button>' +
                      '</td>' +
                    '</tr>';
  return row_element;
}

function changeSponsors() {
  if ($('#create_changeSponsors_form').valid()) {
    var chairs = $('#select_changeSponsors').val();

    var form = new FormData();

    $.each(chairs, function(index, chair) {
      form.append("people", chair);
    });

    var headers = {
      "cache-control": "no-cache"
    }

    var settings = apiRequest(form, headers, server_ip, service_postSponsor, '', true);

    settings['contentType'] = false;
    settings['mimeType'] = 'multipart/form-data';

    $.ajax(settings).done(function (response) {
      console.log('Se crea sponsor correctamente');
      console.log(response);
      getSponsors();
      $('#create_changeSponsors_form').trigger('reset');
      $('#selectSponsors').modal('hide');
    }).fail(function (response) {
      console.log('No se crea correctamente el place');
      console.log(response);
    });
  }
}

function getDevelopers() {
  var settings = apiRequest([], [], server_ip, service_getDeveloper, '', true);

  $.ajax(settings).done(function (response) {
      $('#developers').find('table>tbody').empty();
      $.each(response, function(index, value) {
        $('#developers').find('table>tbody').append(developer_row(value.person_data));
      });
  });
}

function developer_row(element) {
  var row_element = '<tr>' +
                      '<td><img src="{0}" class="img-responsive" style="max-width: 50px;"/></td>'.format(element.photo_url) +
                      '<td>{0} {1}</td>'.format(element.name, element.surname) +
                      '<td>{0}</td>'.format(element.email) +
                      '<td>{0}</td>'.format(element.phone) +
                      '<td class="td-actions text-right">' +
                        '<button type="button" rel="tooltip" title="Edit" class="btn btn-primary btn-simple btn-xs" onclick="editPlace({0})">'.format(element.id) +
                          '<i class="material-icons">edit</i>' +
                        '</button>' +
                        '<button type="button" rel="tooltip" title="Remove" class="btn btn-danger btn-simple btn-xs" onclick="deletePlace({0})">'.format(element.id) +
                          '<i class="material-icons">close</i>' +
                        '</button>' +
                      '</td>' +
                    '</tr>';
  return row_element;
}

function changeDevelopers() {
  if ($('#create_changeDevelopers_form').valid()) {
    var chairs = $('#select_changeDevelopers').val();

    var form = new FormData();

    $.each(chairs, function(index, chair) {
      form.append("people", chair);
    });

    var headers = {
      "cache-control": "no-cache"
    }

    var settings = apiRequest(form, headers, server_ip, service_postDeveloper, '', true);

    settings['contentType'] = false;
    settings['mimeType'] = 'multipart/form-data';

    $.ajax(settings).done(function (response) {
      console.log('Se crea developer correctamente');
      console.log(response);
      getDevelopers();
      $('#create_changeDevelopers_form').trigger('reset');
      $('#selectDevelopers').modal('hide');
    }).fail(function (response) {
      console.log('No se crea correctamente el place');
      console.log(response);
    });
  }
}

function getStreams() {
  var settings = apiRequest([], [], server_ip, service_getStream, '', true);

  $.ajax(settings).done(function (response) {
      $('#stream').find('table>tbody').empty();
      $.each(response, function(index, value) {
        $('#stream').find('table>tbody').append(stream_row(value));
      });
  });
}

function stream_row(element) {
  var row_element = '<tr>' +
                      '<td>{0}</td>'.format(element.description) +
                      '<td>{0}</td>'.format(element.url) +
                      '<td class="td-actions text-right">' +
                        '<button type="button" rel="tooltip" title="Edit" class="btn btn-primary btn-simple btn-xs" onclick="editPlace({0})">'.format(element.id) +
                          '<i class="material-icons">edit</i>' +
                        '</button>' +
                        '<button type="button" rel="tooltip" title="Remove" class="btn btn-danger btn-simple btn-xs" onclick="deletePlace({0})">'.format(element.id) +
                          '<i class="material-icons">close</i>' +
                        '</button>' +
                      '</td>' +
                    '</tr>';
  return row_element;
}

function createStream() {
  if ($('#create_changeStreams_form').valid()) {
    var description = $('#stream_description').val();
    var url = $('#stream_url').val();

    var form = new FormData();

    form.append("description", description);
    form.append("url", url);

    var headers = {
      "cache-control": "no-cache"
    }

    var settings = apiRequest(form, headers, server_ip, service_postStream, '', true);

    settings['contentType'] = false;
    settings['mimeType'] = 'multipart/form-data';

    $.ajax(settings).done(function (response) {
      console.log('Se crea developer correctamente');
      console.log(response);
      getStreams();
      $('#create_changeStreams_form').trigger('reset');
      $('#selectStreams').modal('hide');
    }).fail(function (response) {
      console.log('No se crea correctamente el place');
      console.log(response);
    });
  }
}

function getSketch() {
  var settings = apiRequest([], [], server_ip, service_getSketch, '', true);

  $.ajax(settings).done(function (response) {
      console.log('SKETCH');
      console.log(response);
      $('#sketch_image').attr('src', response.image_url_url);
  });
}

function changeSketch() {
  if ($('#create_changeSketch_form').valid()) {

    var fileInput = $('#sketchImage')[0];
    var sketchImage = fileInput.files[0];

    saveImage(sketchImage, function(image_saved) {
      var description = $('#sketch_description').val();

      var form = new FormData();

      form.append("description", description);
      form.append("image_url", image_saved.id);

      var headers = {
        "cache-control": "no-cache"
      }

      var settings = apiRequest(form, headers, server_ip, service_postSketch, '', true);

      settings['contentType'] = false;
      settings['mimeType'] = 'multipart/form-data';

      $.ajax(settings).done(function (response) {
        console.log('Se crea sketch correctamente');
        console.log(response);
        getSketch();
        $('#create_changeSketch_form').trigger('reset');
        $('#change_sketch').modal('hide');
      }).fail(function (response) {
        console.log('No se crea correctamente el place');
        console.log(response);
      });
    });


  }
}

function getPeople() {
  var settings = apiRequest([], [], server_ip, service_getPeople, '', true);

  $.ajax(settings).done(function (response) {

      $("#select_changeChairs").empty();
      $("#select_changeSponsors").empty();
      $("#select_changeDevelopers").empty();
      $("#select_changeChairs").append('<option disabled >Activity People</option>');
      $("#select_changeSponsors").append('<option disabled >Activity People</option>');
      $("#select_changeDevelopers").append('<option disabled >Activity People</option>');
      $.each(response, function(index, value) {
        console.log('Place');
        console.log(value);
        $("#select_changeChairs").append('<option value={0}>{1}</option>'.format(value.id, value.name));
        $("#select_changeSponsors").append('<option value={0}>{1}</option>'.format(value.id, value.name));
        $("#select_changeDevelopers").append('<option value={0}>{1}</option>'.format(value.id, value.name));
      });
      $('#select_changeChairs').selectpicker('refresh');
      $('#select_changeSponsors').selectpicker('refresh');
      $('#select_changeDevelopers').selectpicker('refresh');
  });
}
