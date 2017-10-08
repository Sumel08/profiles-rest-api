$(document).ready(function() {

  getEventName();
  updatePlaceCategoryTable();
  updatePlaceTable();

});

function updatePlaceTable() {
  var settings = apiRequest([], [], server_ip, service_getPlace, '', true);

  $.ajax(settings).done(function (response) {
      console.log(response);
      $('#place-tab').find('table>tbody').empty();
      $.each(response, function(index, value) {
        console.log(value);
        $('#place-tab').find('table>tbody').append(place_row(value));
      });
  });
}

function place_row(element) {
  var row_element = '<tr>' +
                      '<td><img src="{0}" class="img-responsive" style="max-width: 50px;"/></td>'.format(element.image_url) +
                      '<td>{0}</td>'.format(element.name) +
                      '<td>{0}</td>'.format(element.email) +
                      '<td>{0}</td>'.format(element.telephone) +
                      '<td>{0}</td>'.format(element.place_category_name) +
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

function createPlace() {
  if ($('#create_place_form').valid()) {
    console.log('Es válido');

    var fileInput = $('#place_image')[0];
    var place_image = fileInput.files[0];

    saveImage(place_image, function(image_saved) {
      console.log('Imagen creada correctamente');
      console.log(image_saved.id);
      console.log(image_saved.image);

      var place_name = $('#placeName').val();
      var place_email = $('#placeEmail').val();
      var place_telephone = $('#placeTelephone').val();
      var place_website = $('#placeWebsite').val();
      var place_latitude = $('#placeLatitude').val();
      var place_longitude = $('#placeLongitude').val();
      var place_altitude = $('#placeAltitude').val();
      var place_place_category = $("#select_placeCategory").val();
      var place_description = $('#placeDescription').val();
      var place_additional_info = $('#placeAdditional').val();
      var place_image = image_saved.id;
      var place_indication = $('#placeIndication').val();

      var form = new FormData();
      form.append("name", place_name);
      form.append("email", place_email);
      form.append("telephone", place_telephone);
      form.append("website", place_website);
      form.append("latitude", place_latitude);
      form.append("longitude", place_longitude);
      form.append("altitude", place_altitude);
      form.append("place_category", place_place_category);
      form.append("description", place_description);
      form.append("additional_info", place_additional_info);
      form.append("image", place_image);
      form.append("indication", place_indication);

      var headers = {
        "cache-control": "no-cache"
      }

      var settings = apiRequest(form, headers, server_ip, service_createPlace, '', true);

      settings['contentType'] = false;
      settings['mimeType'] = 'multipart/form-data';

      $.ajax(settings).done(function (response) {
        console.log('Se crea place correctamente');
        console.log(response);
        updatePlaceTable();
        $('#create_place_form').trigger('reset');
        $('#createPlace').modal('hide');
      }).fail(function (response) {
        console.log('No se crea correctamente el place');
        console.log(response);
      });

    });

  } else {
    swal('Fill the form', 'Please fill all the required fields', 'error');
  }
}

function editPlace(element_id) {
  console.log(element_id);
}

function deletePlace(element_id) {
  var settings = apiRequest([], [], server_ip, service_deletePlace, element_id, true);

  $.ajax(settings).done(function (response) {
    updatePlaceTable();
  }).fail(function (response) {
    console.log('No se elimina correctamente la categoría');
    console.log(response);
  });
}

function updatePlaceCategoryTable() {
  var settings = apiRequest([], [], server_ip, service_getPlaceCategory, '', true);

  $.ajax(settings).done(function (response) {
      console.log(response);
      $('#placeCategory-tab').find('table>tbody').empty();
      $("#select_placeCategory").empty();
      $("#select_placeCategory").append('<option disabled selected>Place category</option>');
      $.each(response, function(index, value) {
        console.log(value);
        $('#placeCategory-tab').find('table>tbody').append(placeCategory_row(value));

        $("#select_placeCategory").append('<option value={0}>{1}</option>'.format(value.id, value.name));
      });
  });
}

function placeCategory_row(element) {
  var row_element = '<tr>' +
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

function createPlaceCategory() {
  if ($('#create_placeCategory_form').valid()) {
    var category_name = $('#categoryName').val();
    var category_show_in_app = $('#categoryInApp').is(':checked');
    var category_description = $('#categoryDescription').val();

    var form = new FormData();
    form.append("name", category_name);
    form.append("description", category_description);
    form.append("show_in_app", category_show_in_app);

    var headers = {
      "cache-control": "no-cache"
    }

    var settings = apiRequest(form, headers, server_ip, service_postPlaceCategory, '', true);

    settings['contentType'] = false;
    settings['mimeType'] = 'multipart/form-data';

    $.ajax(settings).done(function (response) {
      $('#create_placeCategory_form').trigger('reset');
      updatePlaceCategoryTable();
      $('#createPlaceCategory').modal('hide');
    }).fail(function (response) {
      console.log('No se crea correctamente la categoría');
      console.log(response);
    });
  } else {

  }
}

function editPlaceCategory(element_id) {
  console.log(element_id);
}

function deletePlaceCategory(element_id) {
  var settings = apiRequest([], [], server_ip, service_deletePlaceCategory, element_id, true);

  $.ajax(settings).done(function (response) {
    updatePlaceCategoryTable();
  }).fail(function (response) {
    console.log('No se elimina correctamente la categoría');
    console.log(response);
  });
}
