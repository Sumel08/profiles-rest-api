$(document).ready(function() {
  var data = {};
  var headers = {};

  var settings = apiRequest(data, headers, server_ip, service_myEvent, '', true);
  console.log(settings);
  $.ajax(settings).done(function (response) {
      console.log(response);
      $('#event_title').html(response.name);
  }).fail(function(jqXHR, textStatus, errorThrown) {
      goPage('create_event');
      //console.log(textStatus);
  });
});
