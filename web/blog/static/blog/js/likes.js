let NotActiveStyle = "font-size:24px"
let ActiveStyle = "font-size:24px;color:red"
let ApiEndPoint = "/actions/assessment/"
let ArticleLikeType = "article"
let LikeVote = 1
let DislikeVote = 0
let flagDislike = 0
let normalLikeCount = Number($("#articleLikeCount").text())
let likePlusOne = Number($("#articleLikeCount").text()) + 1
let likeMinusOne = Number($("#articleLikeCount").text()) - 1

$(function () {
  if ($('#articleLikeCount').attr("data-vote") === "1") {
    $("#articleLikeIcon").attr("style", ActiveStyle);
  } else {
    $("#articleLikeIcon").attr("style", NotActiveStyle);
  }
  if ($('#articleDislikeCount').attr("data-vote") === "0") {
    $("#articleDislikeIcon").attr("style", ActiveStyle);
  } else {
    $("#articleDislikeIcon").attr("style", NotActiveStyle);
  }
  $('#articleLikeIcon').click(getLikeIcon);
  $('#articleDislikeIcon').click(getDislikeIcon);
});

function postLike() {
  $.ajax({
      url: ApiEndPoint,
      type: "POST",
      dataType: 'json',
      data: {
        "like_type": ArticleLikeType,
        "object_id": $("#articleLikeCount").attr("data"),
        "vote": LikeVote,
      },
    })
}

function postDislike() {
  $.ajax({
      url: ApiEndPoint,
      type: "POST",
      dataType: 'json',
      data: {
        "like_type": ArticleLikeType,
        "object_id": $("#articleLikeCount").attr("data"),
        "vote": DislikeVote,
      },
    })
}

function getLikeIcon(e) {

  if ($("#articleDislikeIcon").attr("style") === ActiveStyle) {
    $("#articleDislikeIcon").attr("style", NotActiveStyle);
    if ($('#articleDislikeCount').attr("data-vote") === "0" && flagDislike === 0) {
      let dislikeCount = Number($("#articleDislikeCount").text()) - 1
      $("#articleDislikeCount").text("");
      $("#articleDislikeCount").text(" " + dislikeCount);
      flagDislike = 1
    }
  }

  if ($("#articleLikeIcon").attr("style") === NotActiveStyle) {
    $("#articleLikeIcon").attr("style", ActiveStyle);
    postLike();
    $("#articleLikeCount").text("");
    $("#articleLikeCount").text(" " + likePlusOne);
  } else {
    $("#articleLikeIcon").attr("style", NotActiveStyle);
    postLike();
    $("#articleLikeCount").text("");
    $("#articleLikeCount").text(" " + likeMinusOne);
  }
}

function getDislikeIcon(e) {
  if ($("#articleLikeIcon").attr("style") === ActiveStyle) {
    $("#articleLikeIcon").attr("style", NotActiveStyle);
  }

  if ($("#articleDislikeIcon").attr("style") === NotActiveStyle) {
    $("#articleDislikeIcon").attr("style", ActiveStyle);
    postDislike();
  } else {
    $("#articleDislikeIcon").attr("style", NotActiveStyle);
    postDislike();
  }
}
