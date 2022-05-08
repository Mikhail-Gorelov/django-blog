$(function () {
  $('#updateImageInput').change(changeImage);
});
console.log("Hello from profile!");
// TODO: create pagination for article render

function changeImage(e) {
  let fd = new FormData();
  let button = $(this);
  let files = button[0].files;

  if (files.length > 0) {
    fd.append('image', files[0]);
  }
  e.preventDefault();
  $.ajax({
    url: button.data("href"),
    type: "POST",
    contentType: false,
    processData: false,
    data: fd,
    success: function (data) {
      console.log(data);
      $('#userAvatar').attr("src", data.image);
    },
    error: function (data) {
      console.log("error");
    },
  })
}
