$(function () {
    get_comments();
});



function get_comments() {
  let article_id = $("#articleId").data("id")
  url_web = "/comments/" + article_id + "/"
  $.ajax({
    url: url_web,
    type: "GET",
    success: function (data) {
      buttons(data);
      result(data);
    },
})
}
// function successFunc(data) {
//   console.log(data)
//   console.log(data.next_url)
//   console.log(data.previous_url)
//
//   // let a = document.getElementById('previousHref');
//   // if (data.previous_url == null) {
//   //   a.href = "#";
//   // } else {
//   //   a.href = data.previous_url;
//   // }
//   //
//   // let b = document.getElementById('nextHref');
//   //
//   // if (data.next_url == null) {
//   //   b.href = "#";
//   // } else {
//   //   b.href = data.next_url;
//   // }
//
// }

function buttons(data) {
   let a = document.getElementById('previousHref');
  if (data.previous_url == null) {
    a.href = "#";
  } else {
    a.href = data.previous_url;
  }

  let b = document.getElementById('nextHref');

  if (data.next_url == null) {
    b.href = "#";
  } else {
    b.href = data.next_url;
  }
}

function result(data) {
  console.log(data)
}
