$(function () {
    get_comments();
    $('#previousHref').click(getCommentsButton);
    $('#nextHref').click(getCommentsButton);
});

function getCommentsButton(e) {
  let button = $(this);
  let href = button.data("href");
  console.log(href);
  $.ajax({
    url: href,
    type: "GET",
    success: function (data) {
      buttons(data);
      result(data);
    },
})
  e.preventDefault();
}

function get_comments() {
  let article_id = $("#articleId").data("id");
  let url_web = "/comments/" + article_id + "/";
  $.ajax({
    url: url_web,
    type: "GET",
    success: function (data) {
      buttons(data);
      result(data);
    },
})
}

function buttons(data) {
   let a = $("#previousHref");
   let li = $("#prev");
  if (data.previous == null) {
    a.attr("href", "#");
    li.attr("class", "previous disabled");
  } else {
    li.removeClass("previous disabled");
    a.attr("data-href", data.previous);
  }

  let b = $("#nextHref");

  if (data.next == null) {
    //b.prop("disabled", true);
    b.attr("href", "#");
    let li = $("#nex");
    li.attr("class", "next disabled");
  } else {
    li.removeClass("next disabled");
    b.attr("data-href", data.next);
  }
}

function result(data) {
  let concat = "";
  console.log(data);

  for (let i = 0; i < data.results.length; ++i) {
    concat += " <h3><i class=\"fa fa-comment\"></i> "
      + data.results[i].author   +  "<small>" + data.results[i].updated +
      "</small>" + "</h3>" + "<p>" + data.results[i].content + "</p>";
  }
  $('#articleId').html(concat);

}
