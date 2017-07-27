$(document).ready(function() {
  var data = {};
  var headers = {};

  var settings = apiRequest(data, headers, server_ip, service_myEvents, '', true);
  console.log(settings);
  $.ajax(settings).done(function (response) {
      console.log(response);
      $('#events_select').empty();
      $.each(response, function(index, value) {
        if (index == 0)
          localStorage.setItem(event_selected, value.id);
        $('#events_select').append($('<option>', { value : value.id }).text(value.name));
      });
  });
});
