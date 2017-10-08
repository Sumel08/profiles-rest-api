$(document).ready(function() {
  getEventName();
  updatePeopleTable();
  getPlaces();
})

function createPeople() {
  if ($('#create_people_form').valid()) {

    var fileInput = $('#personPhoto')[0];
    var personPhoto = fileInput.files[0];

    saveImage(personPhoto, function(image_saved) {
      var person_name = $('#personName').val();
      var person_surname = $('#personSurname').val();
      var person_email = $('#personEmail').val();
      var person_birthdate = $('#personBirthdate').val();
      var person_phone = $('#personPhone').val();
      var person_provenance = $('#select_personProvenance').val();
      var person_resume = $('#personResume').val();
      var person_photo = image_saved.id;

      var form = new FormData();
      form.append("name", person_name);
      form.append("surname", person_surname);
      form.append("birthdate", person_birthdate);
      form.append("email", person_email);
      form.append("phone", person_phone);
      form.append("resume", person_resume);
      form.append("provenance", person_provenance);
      form.append("photo", person_photo);

      var headers = {
        "cache-control": "no-cache"
      }

      var settings = apiRequest(form, headers, server_ip, service_createPeople, '', true);

      settings['contentType'] = false;
      settings['mimeType'] = 'multipart/form-data';

      $.ajax(settings).done(function (response) {
        console.log('Se crea place correctamente');
        console.log(response);
        updatePeopleTable();
        $('#create_people_form').trigger('reset');
        $('#createPeople').modal('hide');
      }).fail(function (response) {
        console.log('No se crea correctamente el place');
        console.log(response);
      });
    });

  } else {
    swal('Fill the form', 'Please fill all the required fields', 'error');
  }
}

function updatePeopleTable() {
  var settings = apiRequest([], [], server_ip, service_getPeople, '', true);

  $.ajax(settings).done(function (response) {
      console.log(response);
      $('#people-tab').find('table>tbody').empty();
      $.each(response, function(index, value) {
        console.log(value);
        $('#people-tab').find('table>tbody').append(people_row(value));
      });
  });
}

function people_row(element) {
  var row_element = '<tr>' +
                      '<td><img src="{0}" class="img-responsive" style="max-width: 50px;"/></td>'.format(element.photo_url) +
                      '<td>{0} {1}</td>'.format(element.surname, element.name) +
                      '<td>{0}</td>'.format(element.email) +
                      '<td>{0}</td>'.format(element.phone) +
                      '<td>{0}</td>'.format(element.provenance_name) +
                      '<td class="td-actions text-right">' +
                        '<button type="button" rel="tooltip" title="Edit" class="btn btn-primary btn-simple btn-xs" onclick="editPeople({0})">'.format(element.id) +
                          '<i class="material-icons">edit</i>' +
                        '</button>' +
                        '<button type="button" rel="tooltip" title="Remove" class="btn btn-danger btn-simple btn-xs" onclick="deletePeople({0})">'.format(element.id) +
                          '<i class="material-icons">close</i>' +
                        '</button>' +
                      '</td>' +
                    '</tr>';
  return row_element;
}

function getPlaces() {
  var settings = apiRequest([], [], server_ip, service_getPlace, '', true);

  $.ajax(settings).done(function (response) {

      $("#select_personProvenance").empty();
      $("#select_personProvenance").append('<option disabled selected>Select a plce</option>');
      $.each(response, function(index, value) {
        $("#select_personProvenance").append('<option value={0}>{1}</option>'.format(value.id, value.name));
      });
  });
}
