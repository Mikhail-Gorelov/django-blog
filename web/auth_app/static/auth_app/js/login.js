$(function () {
  // $(document).on("click", "a.login", login);
  $('#loginForm').submit(login);
  $('#forgotPasswordForm').submit(forgotPassword);
  $('#forgotPasswordFormSuccess').submit(forgotPasswordSuccess);
});

function recaptchaCallback() {
  $('#signInButton').removeAttr('disabled');
}

function recaptchaCallForgotback() {
  $('#forgotButton').removeAttr('disabled');
}

$('.gallery-overlay').click(function () {
  $(this).fadeOut('slow');
});

$('.gallery-image').click(function () {
  return false;
});

function login(e) {
  let form = $(this);
  e.preventDefault();
  recaptchaCallback();
  $.ajax({
    url: form.attr("action"),
    type: "POST",
    dataType: 'json',
    data: form.serialize(),
    success: function (data) {
      url = '/';
      localStorage.setItem('access_token', data.access_token);
      window.location.href = url;
    },
    error: function (data) {
      if (data.responseJSON.non_field_errors) {
        $("#captchaGroup").addClass("has-error");
        $(".help-block").remove()
        $("#captchaGroup").append(
          '<div class="help-block">' + data.responseJSON.non_field_errors[0] + "</div>"
        );
      } else {
        $("#emailGroup").addClass("has-error");
        $("#passwordGroup").addClass("has-error");
        $(".help-block").remove()
        $("#passwordGroup").append(
          '<div class="help-block">' + data.responseJSON.email + "</div>"
        );
      }
    }
  })
}

function forgotPassword(e) {
  let form = $(this);
  e.preventDefault();
  recaptchaCallForgotback();
  $.ajax({
    url: form.attr("action"),
    type: "POST",
    dataType: 'json',
    data: form.serialize(),
    success: function (data) {
      $('#pwdModal').modal("hide");
      $('#pwdModalSecond').modal("show");
    },
    error: function (data) {
      if (data.responseJSON.non_field_errors) {
        $("#captchaGroupModal").addClass("has-error");
        $(".help-block").remove()
        $("#captchaGroupModal").append(
          '<div class="help-block">' + data.responseJSON.non_field_errors[0] + "</div>"
        );
      }
    },
  })
}

function forgotPasswordSuccess(e) {
  let form = $(this);
  window.location.href = form.attr("action");
}

function buttonAvailable(e) {
  console.log($(".g-recaptcha").val());
  $("#signInButton").disabled = !$(".g-recaptcha");
}
