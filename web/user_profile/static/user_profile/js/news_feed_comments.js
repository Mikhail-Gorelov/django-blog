$(function () {
  getCommentList();
});
$.fn.scrollBottom = function () {
  return $(document).height() - this.scrollTop() - this.height();
};
let requestedNewPageComment = false;
$(document).scroll(function () {
  if ($(this).height() - $(this).scrollTop() < 1000 && !requestedNewPageComment) {
    if ($('.container').attr('data')) {
      requestedNewPageComment = true;
      getCommentList($('.container').attr('data'));
    }
  }
});

function getCommentList(url = null) {
  let url_web = ""

  if (url == null) {
    url_web = $(".container").attr("data-href");
  } else {
    url_web = url;
  }

  $.ajax({
    url: url_web,
    type: "GET",
    success: function (data) {
      commentListRender(data);
    },
  })
}

function commentListRender(data) {
  let commentList = data.results;
  $(".container").attr("data-href", data.next);

  let comments = ``;
  $.each(commentList, function (i) {
    comments += commentListFunc(
      commentList[i].author.image, commentList[i].author.full_name, commentList[i].updated,
      commentList[i].content, commentList[i].article.title, commentList[i].article.slug,);
  })
  $('#commentContainer').append(comments);
  $('.container').attr('data', data.next);
  requestedNewPageArticle = false;
}

function commentListFunc(authorImage, authorFullName, commentUpdated, commentContent, commentTitle, commentSlug) {
  let comment = `
        <section class="py-4">
          <div class="mb-4 py-4">
            <div class="d-flex justify-content-between align-items-center">
              <div class="d-flex flex-row align-items-center">
                <div class="avatar mr-3"><img class="avatar-img" src="${authorImage}"
                                              alt="avatar">
                </div>
                <div>
                  <h2 class="h6 mb-0">${authorFullName}</h2>
                  <p class="small text-muted mb-0">${commentUpdated} ago</p>
                </div>
              </div>
            </div>
            <div class="mt-3">
              <p class="text-muted mb-0"><a href="${commentSlug}"><strong>${commentTitle}</strong></a></p>
              <p class="text-muted mb-0">${commentContent}</p>
            </div>
          </div>
      </section>
  `;
  return comment;
}
