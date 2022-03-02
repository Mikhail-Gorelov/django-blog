let href = $("#updateCredentials").attr("data-href");
let hrefRedirect = $("#updateCredentials").attr("data-redirect");
let backendSite = $("#updateCredentials").attr("data-site");
const error_class_name = "has-error"

$(function () {
  $("#updateCredentials").click(sendCredentials);
});

function validateEmail(email) {
  let mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
  return !!email.match(mailformat);
}

function error_process(email) {
  $(".help-block").remove()
  $("#emailGroup").removeClass(error_class_name);
  help_block("#emailGroup", "Enter valid email");
}

function help_block(group, variable) {
  $(group).addClass(error_class_name);
  $(group).append('<div class="help-block">' + variable + "</div>");
}


function sendCredentials() {
  let name = $("#name").val() === "" ? $("#name").attr("placeholder") : $("#name").val();
  let lastname = $("#lastname").val() === "" ? $("#lastname").attr("placeholder") : $("#lastname").val();
  let email = $("#email").val() === "" ? $("#email").attr("placeholder") : $("#email").val();
  let birthday = $("#birthday").val() === "" ? $("#birthday").attr("placeholder") : $("#birthday").val();
  let website = $("#website").val() === "" ? $("#website").attr("placeholder") : $("#website").val();
  let biography = $("#biography").val() === "" ? $("#biography").attr("placeholder") : $("#biography").val();
  let gender = $("#select :selected").text() === "Male" ? 0 : 1;

  if (validateEmail(email)) {
    $.ajax({
      url: href,
      type: "PUT",
      dataType: 'json',
      data: {
        "first_name": name,
        "last_name": lastname,
        "email": email,
        "birthday": birthday,
        "gender": gender,
        "website": website,
        "biography": biography,
      },
      success: function () {
        window.location.replace(backendSite);
      },
      error: function (data) {
        window.location.replace(backendSite);
      },
    })
  } else {
    error_process(email);
  }

}
