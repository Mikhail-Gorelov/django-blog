$(function () {
  $('#signUpForm').submit(singUp);
  $('#buttonForm').submit(button_process);
});
const error_class_name = "has-error"

function recaptchaCallback() {
  $('#signUpButton').removeAttr('disabled');
}

function singUp(e) {
  let form = $(this);
  e.preventDefault();
  recaptchaCallback();
  $.ajax({
    url: form.attr("action"),
    type: form.attr("method"),
    dataType: 'json',
    data: form.serialize(),
    success: function (data) {
      button_process(data)
    },
    error: function (data) {
      error_process(data);
    }
  })
}

function error_process(data) {
  $(".help-block").remove()
  let groups = ['#emailGroup', '#password1Group', '#password2Group', '#firstNameGroup',
    '#lastNameGroup', '#birthdayGroup', '#genderGroup'];

  for (let group of groups) {
    $(group).removeClass(error_class_name);
  }
  if (data.responseJSON.email) {
    help_block("#emailGroup", data.responseJSON.email)
  }
  if (data.responseJSON.password1) {
    help_block("#password1Group", data.responseJSON.password1)
  }
  if (data.responseJSON.password2) {
    help_block("#password2Group", data.responseJSON.password2)
  }
  if (data.responseJSON.first_name) {
    help_block("#firstNameGroup", data.responseJSON.first_name)
  }
  if (data.responseJSON.last_name) {
    help_block("#lastNameGroup", data.responseJSON.last_name)
  }
  if (data.responseJSON.birthdate) {
    help_block("#birthdayGroup", data.responseJSON.birthdate)
  }
  if (data.responseJSON.gender) {
    help_block("#genderGroup", data.responseJSON.gender)
  }
  if (data.responseJSON.non_field_errors) {
    help_block("#captchaGroup", data.responseJSON.non_field_errors[0])
  }
}

function help_block(group, variable) {
  $(group).addClass(error_class_name);
  $(group).append('<div class="help-block">' + variable + "</div>");
}

function button_process(data) {
  $('#clickMe').click(function () {
    window.location.href = "/auth/login";
  });
}
