$(function () {
  // $(document).on("click", "a.login", login);
  $('#loginForm').submit(login);
  $('#forgotPasswordForm').submit(forgotPassword);
  $('#forgotPasswordFormSuccess').submit(forgotPasswordSuccess)
});
$('.gallery-overlay').click(function() {
    $(this).fadeOut('slow');
});

$('.gallery-image').click(function() {
    return false;
});
function login(e) {
  let form = $(this);
  e.preventDefault();
  $.ajax({
    url: form.attr("action"),
    type: "POST",
    dataType: 'json',
    data: form.serialize(),
    success: function (data) {
      url = '/';
      window.location.href = url;
    },
    error: function (data) {
      $("#emailGroup").addClass("has-error");
      $("#passwordGroup").addClass("has-error");
      $(".help-block").remove()
      $("#passwordGroup").append(
        '<div class="help-block">' + data.responseJSON.email + "</div>"
      );

    }
  })
  console.log(form.data())
}
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
      $('#pwdModal').modal("hide");
      $('#pwdModalSecond').modal("show");
      console.log(data, "success");
    },
    error: function (data) {
      console.log(data, "error");
    },
  })
}
function forgotPasswordSuccess(e) {
  let form = $(this);
  window.location.href = form.attr("action");
}
