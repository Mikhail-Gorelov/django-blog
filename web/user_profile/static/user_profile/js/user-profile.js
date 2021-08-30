$(function () {
  $('#updateImageInput').change(changeImage);
  $('#gender').change(changeInformation);
  $('#birthdate').change(changeInformation);
  $('#bio').change(changeInformation);
  $('#website').change(changeInformation);
});

function changeImage(e) {
  let fd = new FormData();
  let button = $(this);
  let files = button[0].files;

  // Check file selected or not
  if(files.length > 0 ){
      fd.append('image',files[0]);
  }
  e.preventDefault();
  // let formData = new FormData(form[0]);
  //console.log(form.data);
  // console.log(form.serialize());
  // console.log(formData);
  // console.log(form);
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

function changeInformation(e) {
  let field = $(this);
  e.preventDefault();
  console.log(field);
  console.log(field[0].value);
  console.log(field[0].id);
  let myVal = field[0].value;
  let myKey = field[0].id;
  myKey.toString();
  myVal.toString();
  // console.log("field[0].value");
  // console.log("field[0].id");
  // надо подать именно то поле, которое id {'id' : field.value}
  $.ajax({
    url: field.data("href"),
    type: "PUT",
    data:  {myKey: myVal},
    success: function (e) {
      console.log("success");
    },
    error: function (data) {
      console.log(data.responseText);
    },
  })


}
