$(function () {
  $('#updataImageInput').change(changeImage);
});

function changeImage(e) {
  let fd = new FormData();
  let files = $('#updataImageInput')[0].files;

  // Check file selected or not
  if(files.length > 0 ){
      fd.append('file',files[0])
  }
  // let form = $(this);
  e.preventDefault();
  // let formData = new FormData(form[0]);
  //console.log(form.data);
  // console.log(form.serialize());
  // console.log(formData);
  // console.log(form);
  $.ajax({
    url: "/user-profile/update-image/",
    type: "POST",
    contentType: false,
    processData: false,
    data: fd,
    success: function (e) {
     console.log(fd);
     window.location.reload();
    },
    error: function (data) {
     console.log("error");
    },
  })
}
