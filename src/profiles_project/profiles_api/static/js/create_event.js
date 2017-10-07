function create_event() {
  if ($('#create_event_form').valid()) {
    console.log('Es válido');

    var fileInput = $('#event_image')[0];
    var event_image = fileInput.files[0];

    saveImage(event_image, function(image_saved) {
      console.log('Imagen creada correctamente');
      console.log(image_saved.id);
      console.log(image_saved.image);

      var event_name = $('#name').val();
      var event_code = $('#code').val();
      var event_description = $('#description').val();
      var start_date = $('#start_date').val();
      var end_date = $('#end_date').val();

      var form = new FormData();
      form.append("event_image", "1");
      form.append("start_date", start_date);
      form.append("end_date", end_date);
      form.append("name", event_name);
      form.append("code", event_code);
      form.append("description", event_description);

      var headers = {
        "cache-control": "no-cache"
      }

      var settings = apiRequest(form, headers, server_ip, service_createEvent, '', true);

      settings['contentType'] = false;
      settings['mimeType'] = 'multipart/form-data';

      $.ajax(settings).done(function (response) {
        console.log('Se crea evento correctamente');
        console.log(response);
        goPage('dashboard');
      }).fail(function (response) {
        console.log('No se crea correctamente el evento');
        console.log(response);
      });

    });

  } else {
    swal('Fill the form', 'Please fill all the required fields', 'error');
  }
}
