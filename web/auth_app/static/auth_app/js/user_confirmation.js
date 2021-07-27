$(function () {
  $('#successForm').submit(successFunc);
});
let url = window.location.href;
let code = url.split("/");
console.log(code[5]);
function successFunc(e) {
  let form = $(this);
  e.preventDefault();
  $.ajax({
    url: form.attr("action"),
    type: "POST",
    dataType: 'json',
    data: {"key": code[5]},
    success: function (e) {
      url = "/auth/login/";
      window.location.href = url;
    },
    error: function (data) {
      error_process(data);
    },
  })
}

function error_process(data) {
  console.log(data.responseText);
}
