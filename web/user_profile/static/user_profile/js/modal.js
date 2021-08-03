$(function () {
  $('#forgotPasswordForm').submit(forgotPassword);
});
$('.gallery-overlay').click(function() {
    $(this).fadeOut('slow');
});

$('.gallery-image').click(function() {
    return false;
});
function forgotPassword(e) {
  console.log("Here");
  let form = $(this);
  e.preventDefault();
  $.ajax({
    url: form.attr("action"),
    type: "POST",
    dataType: 'json',
    data: form.serialize(),
    success: function (data) {
      console.log(data, "success");
      url = '/auth/login/';
      window.location.href = url;
    },
    error: function (data) {
      console.log(data, "error");
    },
  })
}

