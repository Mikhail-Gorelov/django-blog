let NotActiveStyle = "font-size:24px"
let ActiveStyle = "font-size:24px;color:red"
let ApiEndPoint = "/actions/assessment/"
let ArticleLikeType = "article"
let LikeVote = 1
let DislikeVote = 0

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
      success: function (data) {
        $("#articleLikeCount").text("");
        $("#articleLikeCount").text(" " + data.likes_count);
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
      success: function (data) {
        $("#articleDislikeCount").text("");
        $("#articleDislikeCount").text(" " + data.dislike_count);
      },
    })
}

function getLikeIcon(e) {

  if ($("#articleDislikeIcon").attr("style") === ActiveStyle) {
    $("#articleDislikeIcon").attr("style", NotActiveStyle);
    let dislikeCount = Number($("#articleDislikeCount").text()) - 1
    $("#articleDislikeCount").text("");
    $("#articleDislikeCount").text(" " + dislikeCount);
  }

  if ($("#articleLikeIcon").attr("style") === NotActiveStyle) {
    $("#articleLikeIcon").attr("style", ActiveStyle);
    postLike();
  } else {
    $("#articleLikeIcon").attr("style", NotActiveStyle);
    postLike();
  }
}

function getDislikeIcon(e) {
  if ($("#articleLikeIcon").attr("style") === ActiveStyle) {
    $("#articleLikeIcon").attr("style", NotActiveStyle);
    let likeCount = Number($("#articleLikeCount").text()) - 1
    $("#articleLikeCount").text("");
    $("#articleLikeCount").text(" " + likeCount);
    }

  if ($("#articleDislikeIcon").attr("style") === NotActiveStyle) {
    $("#articleDislikeIcon").attr("style", ActiveStyle);
    postDislike();
  } else {
    $("#articleDislikeIcon").attr("style", NotActiveStyle);
    postDislike();
  }
}
