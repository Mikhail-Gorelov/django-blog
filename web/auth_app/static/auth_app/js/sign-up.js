console.log('sing-up')
$(function () {
  $('#signUpForm').submit(singUp);
});

function singUp(e) {
  let form = $(this);
  e.preventDefault();
  console.log('here')
  let path = form.attr("action")
  console.log(path)
  let method = form.attr("method")
  let data = form.serialize()
  console.log(data)
  $.ajax({
    url: path,
    type: method,
    data: data,
    success: function (data){
      console.log('success',data)
    },
    error: function (data){
      console.log('error',data)
      errorProcess(data)
    }
  })
}
function errorProcess(data) {
  $(".help-block").remove()
  if (data.responseJSON.first_name) {
    $("#firstNameGroup").append("<div class='help-block'>"+data.responseJSON.first_name+"</div>")
    $("#firstNameGroup").addClass("has-error")
  }
  if (data.responseJSON.last_name) {
    $("#lastNameGroup").append("<div class='help-block'>"+data.responseJSON.last_name+"</div>")
    $("#lastNameGroup").addClass("has-error")
  }
  if (data.responseJSON.email) {
    $("#emailGroup").append("<div class='help-block'>"+data.responseJSON.email+"</div>")
    $("#emailGroup").addClass("has-error")
  }
  if (data.responseJSON.password1) {
    $("#passwordGroup").append("<div class='help-block'>"+data.responseJSON.password1+"</div>")
    $("#passwordGroup").addClass("has-error")
  }
  if (data.responseJSON.password2) {
    $("#passwordGroup").append("<div class='help-block'>"+data.responseJSON.password2+"</div>")
    $("#passwordGroup").addClass("has-error")
  }

}
