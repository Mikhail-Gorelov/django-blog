$(function () {
  $('#contactUsForm').submit(contactUs);
});
const error_class_name = "has-error"
function contactUs(e) {
  let form = $(this)
  console.log(form.serialize())
  e.preventDefault();
  let formData = new FormData(form[0]);
  $.ajax({
    url: form.attr("action"),
    type: "POST",
    contentType: false,
    processData: false,
    data: formData,
    success: function (data) {
      url = '/';
      window.location.href = url;
      // console.log("success");
    },
    error: function (data) {
      error_process(data);
    }
  })
}
function error_process(data) {
  $(".help-block").remove()
  let groups = ['#nameGroup', '#emailGroup', '#contentGroup']
  for (let group of groups) {
    $(group).removeClass(error_class_name);
  }
  if (data.responseJSON.name) {
    help_block("#nameGroup", data.responseJSON.name);
  }
  if (data.responseJSON.email) {
    help_block("#emailGroup", data.responseJSON.email);
  }
  if (data.responseJSON.content) {
    help_block("#contentGroup", data.responseJSON.content);
  }
}
function help_block(group, variable) {
  $(group).addClass(error_class_name);
  $(group).append('<div class="help-block">' + variable + "</div>");
}
