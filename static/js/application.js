// Support TLS-specific URLs, when appropriate.
if (window.location.protocol == "https:") {
  var ws_scheme = "wss://";
} else {
  var ws_scheme = "ws://"
};

var outbox = new ReconnectingWebSocket(ws_scheme + location.host + "/submit");

outbox.onmessage = function(message) {
  var data = JSON.parse(message.data);
  $("#messages").append("<div class='panel panel-default'><div class='panel-heading'>" + data.data + "</div></div>");
  window.scrollTo( 0, $("body").height() ) ;
};

outbox.onclose = function(){
    console.log('outbox closed');
    this.outbox = new WebSocket(outbox.url);
};

$("#input-form").on("submit", function(event) {
  event.preventDefault();
  var text   = $("#input-text")[0].value;
  outbox.send(text);
  $("#input-text")[0].value = "";
});

$(function() {
  $(window).on('scroll', function() {
    if ($(this).scrollTop() > 50) {
      $('.fixing-base').addClass('fixed');
    } else {
      $('.fixing-base').removeClass('fixed');
    }
  });
});