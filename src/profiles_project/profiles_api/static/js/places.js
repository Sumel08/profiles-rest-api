$(document).ready(function() {

  getEventName();
  updatePlaceCategoryTable();

});

function updatePlaceCategoryTable() {
  var settings = apiRequest([], [], server_ip, service_getPlaceCategory, '', true);

  $.ajax(settings).done(function (response) {
      console.log(response);
      $('#placeCategory-tab').find('table>tbody').empty();
      $.each(response, function(index, value) {
        console.log(value);
        $('#placeCategory-tab').find('table>tbody').append(placeCategory_row(value));
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
      console.log('Se crea categoría correctamente');
      console.log(response);
      updatePlaceCategoryTable();
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
  console.log(element_id);
}
