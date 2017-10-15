$(document).ready(function() {
  getEventName();
  updateActivityTypeTable();
  updateActivityTable();
  getPlaces();
  getPeople();
})

function createActivity() {
  if ($('#create_activity_form').valid()) {
    console.log('Es válido');

    var activity_title = $('#activityTitle').val();
    var activity_subtitle = $('#activitySubtitle').val();
    var activity_start_date = $('#start_date').val();
    var activity_end_date = $('#end_date').val();
    var activity_description = $('#activityDescription').val();
    var activity_notes = $('#activityNotes').val();
    var activity_place = $('#select_activityPlace').val();
    var activity_activity_type = $('#select_activityType').val();
    var activity_price = $('#activityPrice').val();

    if (isNaN(parseFloat(activity_price))) {
      activity_price = 0;
    }

    var form = new FormData();
    form.append("title", activity_title);
    form.append("subtitle", activity_subtitle);
    form.append("start_date", activity_start_date);
    form.append("end_date", activity_end_date);
    form.append("description", activity_description);
    form.append("notes", activity_notes);
    form.append("place", activity_place);
    form.append("activity_type", activity_activity_type);
    form.append("price", activity_price);

    var headers = {
      "cache-control": "no-cache"
    }

    var settings = apiRequest(form, headers, server_ip, service_postActivity, '', true);

    settings['contentType'] = false;
    settings['mimeType'] = 'multipart/form-data';

    $.ajax(settings).done(function (response) {
      console.log('Se crea activity correctamente');
      response = jQuery.parseJSON(response);
      console.log(response);
      var activity_people = $('#select_activityPeople').val();
      var form2 = new FormData();

      form2.append('activity', response.id)
      $.each(activity_people, function(index, value) {
        form2.append('person', value)
      });

      settings = apiRequest(form2, headers, server_ip, service_postActivityPeople, '', true);

      settings['contentType'] = false;
      settings['mimeType'] = 'multipart/form-data';

      $.ajax(settings).done(function (response) {
        console.log('Se crea activity people correctamente');
        console.log(response);

        updateActivityTable();
        $('#create_activity_form').trigger('reset');
        $('#createActivity').modal('hide');
      }).fail(function (response) {
        console.log('Activity people salió mal');
        console.log(response);
      })

    }).fail(function (response) {
      console.log('No se crea correctamente el place');
      console.log(response);
    });

  } else {
    swal('Fill the form', 'Please fill all the required fields', 'error');
  }
}

function updateActivityTable() {
  var settings = apiRequest([], [], server_ip, service_getActivity, '', true);

  $.ajax(settings).done(function (response) {
      console.log(response);
      $('#place-tab').find('table>tbody').empty();
      $.each(response, function(index, value) {
        console.log(value);
        $('#place-tab').find('table>tbody').append(activity_row(value));
      });
  });
}

function activity_row(element) {
  var row_element = '<tr>' +
                      '<td><img src="{0}" class="img-responsive" style="max-width: 50px;"/></td>'.format(element.activity_type_image) +
                      '<td>{0}</td>'.format(element.title) +
                      '<td>{0}</td>'.format(element.activity_type_name) +
                      '<td>{0}</td>'.format(element.place_name) +
                      '<td>{0}</td>'.format(element.date) +
                      '<td>{0}</td>'.format(element.price) +
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

function updateActivityTypeTable() {
  var settings = apiRequest([], [], server_ip, service_getActivityType, '', true);

  $.ajax(settings).done(function (response) {
      console.log(response);
      $('#placeCategory-tab').find('table>tbody').empty();
      $("#select_activityType").empty();
      $("#select_activityType").append('<option disabled selected>Activity Type</option>');
      $.each(response, function(index, value) {
        console.log(value);
        $('#placeCategory-tab').find('table>tbody').append(activityType_row(value));

        $("#select_activityType").append('<option value={0}>{1}</option>'.format(value.id, value.name));
      });
      $('#select_activityType').selectpicker('refresh');
  });
}

function activityType_row(element) {
  var row_element = '<tr>' +
                      '<td><img src="{0}" class="img-responsive" style="max-width: 50px;"/></td>'.format(element.image_url) +
                      '<td>{0}</td>'.format(element.name) +
                      '<td>{0}</td>'.format(element.description) +
                      '<td>{0}</td>'.format(element.show_in_app?'Shown':'Hidden') +
                      '<td class="td-actions text-right">' +
                        '<button type="button" rel="tooltip" title="Edit" class="btn btn-primary btn-simple btn-xs" onclick="editPlaceCategory({0})">'.format(element.id) +
                          '<i class="material-icons">edit</i>' +
                        '</button>' +
                        '<button type="button" rel="tooltip" title="Remove" class="btn btn-danger btn-simple btn-xs" onclick="deletePlaceCategory({0})">'.format(element.id) +
                          '<i class="material-icons">close</i>' +
                        '</button>' +
                      '</td>' +
                    '</tr>';
  return row_element;
}

function createActivityType() {
  if ($('#create_activityType_form').valid()) {

    var fileInput = $('#activityTypeImage')[0];
    var personPhoto = fileInput.files[0];

    saveImage(personPhoto, function(image_saved) {

      var category_name = $('#categoryName').val();
      var category_show_in_app = $('#categoryInApp').is(':checked');
      var category_description = $('#categoryDescription').val();

      var form = new FormData();
      form.append("name", category_name);
      form.append("description", category_description);
      form.append("show_in_app", category_show_in_app);
      form.append("image", image_saved.id);

      var headers = {
        "cache-control": "no-cache"
      }

      var settings = apiRequest(form, headers, server_ip, service_postActivityType, '', true);

      settings['contentType'] = false;
      settings['mimeType'] = 'multipart/form-data';

      $.ajax(settings).done(function (response) {
        $('#create_activityType_form').trigger('reset');
        updateActivityTypeTable();
        $('#createActivityType').modal('hide');
      }).fail(function (response) {
        console.log('No se crea correctamente la categoría');
        console.log(response);
      });
    });
  } else {

  }
}

function getPlaces() {
  var settings = apiRequest([], [], server_ip, service_getPlace, '', true);

  $.ajax(settings).done(function (response) {

      $("#select_activityPlace").empty();
      $("#select_activityPlace").append('<option disabled selected>Activity Place</option>');
      $.each(response, function(index, value) {
        console.log('Place');
        console.log(value);
        $("#select_activityPlace").append('<option value={0}>{1}</option>'.format(value.id, value.name));
      });
      $('#select_activityPlace').selectpicker('refresh');
  });
}

function getPeople() {
  var settings = apiRequest([], [], server_ip, service_getPeople, '', true);

  $.ajax(settings).done(function (response) {

      $("#select_activityPeople").empty();
      $("#select_activityPeople").append('<option disabled >Activity People</option>');
      $.each(response, function(index, value) {
        console.log('Place');
        console.log(value);
        $("#select_activityPeople").append('<option value={0}>{1}</option>'.format(value.id, value.name));
      });
      $('#select_activityPeople').selectpicker('refresh');
  });
}
