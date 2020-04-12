window.addEventListener("wheel", function(event) {
  if (event.deltaY < 0) {
    $("#header_logo").show();
  } else if (event.deltaY > 0 && $(document).height() > $(window).height()) {
    $("#header_logo").hide();
  }
});

function showError(msg) {
  //$("#main-container").append("<h1 class=\"display-4\" style=\"font-size: 28px;\">No Flights Available. Please try searching again.</h1>");

  $("#errorDiv").empty();
  $("#errorDiv").append(
    '<div class="alert alert-danger alert-dismissible fade show" role="alert">' +
      msg +
      `<button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button></div>`
  );
  $("#header_logo").show();
  $(window).scrollTop(0);
}
