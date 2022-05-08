$(function () {
  getFollowerList();
});
$.fn.scrollBottom = function () {
  return $(document).height() - this.scrollTop() - this.height();
};
let requestedNewPageFollower = false;
$(document).scroll(function () {
  if ($(this).height() - $(this).scrollTop() < 1000 && !requestedNewPageFollower) {
    if ($('.container').attr('data')) {
      requestedNewPageFollower = true;
      getFollowerList($('.container').attr('data'));
    }
  }
});

function getFollowerList(url = null) {
  let url_web = ""

  if (url == null) {
    url_web = $(".container").attr("data-href");
  } else {
    url_web = url;
  }
  console.log(url_web);

  $.ajax({
    url: url_web,
    type: "GET",
    success: function (data) {
      followerListRender(data);
    },
  })
}

function followerListRender(data) {
  let followerList = data.results;
  $(".container").attr("data-href", data.next);

  let followers = ``;
  $.each(followerList, function (i) {
    if (followerList[i].content_type.article) {
      followers += followerListFunc(
        followerList[i].content_type.author.image, followerList[i].content_type.author.full_name,
        followerList[i].content_type.updated, followerList[i].content_type.image, followerList[i].content_type.title,
        followerList[i].content_type.content, followerList[i].user.image, followerList[i].user.full_name,
        followerList[i].vote, followerList[i].content_type.type, followerList[i].content_type.article.title,
        followerList[i].content_type.article.slug);
    } else {
      followers += followerListFunc(
        followerList[i].content_type.author.image, followerList[i].content_type.author.full_name,
        followerList[i].content_type.updated, followerList[i].content_type.image, followerList[i].content_type.title,
        followerList[i].content_type.content, followerList[i].user.image, followerList[i].user.full_name,
        followerList[i].vote, followerList[i].content_type.type,);
    }
  })
  $('#likeContainer').append(followers);
  $('.container').attr('data', data.next);
  requestedNewPageFollower = false;
}

function followerListFunc(authorImage, authorFullName, blogUpdated, blogImage, blogTitle, blogContent, likeImage,
                          likeAuthorFullName, vote, type, commentTitle, commentSlug) {

  let like_dislike = ``;
  if (vote === 1) {
    like_dislike = `
    <h2 class="h6 mb-0">${likeAuthorFullName}</h2>
    <p class="small text-muted mb-0">Liked this</p>
    `;
  } else {
    like_dislike = `
    <h2 class="h6 mb-0">${likeAuthorFullName}</h2>
    <p class="small text-muted mb-0">Disliked this</p>
    `;
  }

  let contentType = ``;
  if (type === "article") {
    contentType = `
      <section class="py-4">
          <div class="mb-4 py-4">
            <div class="d-flex justify-content-between align-items-center">
              <div class="d-flex flex-row align-items-center">
                <div class="avatar mr-3"><img class="avatar-img" src="${authorImage}"
                                              alt="avatar">
                </div>
                <div>
                  <h2 class="h6 mb-0">${authorFullName}</h2>
                  <p class="small text-muted mb-0">${blogUpdated} ago</p>
                </div>
              </div>
            </div>
            <img class="rounded w-100 mt-3" src="${blogImage}" alt="feed">
            <div class="mt-3">
              <h4 class="h5"> ${blogTitle} </h4>
              <p class="text-muted mb-0">${blogContent}</p>
            </div>
            <div class="mt-3">
              <div class="d-flex flex-row align-items-center">
                <div class="avatar mr-3"><img class="avatar-img" src="${likeImage}"
                                              alt="avatar">
                </div>
                <div>
                ${like_dislike}
                </div>
              </div>
            </div>
          </div>
      </section>
    `;
  } else {
    contentType = `
        <section class="py-4">

            <div class="mb-4 py-4">
            <div class="d-flex justify-content-between align-items-center">
              <div class="d-flex flex-row align-items-center">
                <div class="avatar mr-3"><img class="avatar-img" src="${authorImage}"
                                              alt="avatar">
                </div>
                <div>
                  <h2 class="h6 mb-0">${authorFullName}</h2>
                  <p class="small text-muted mb-0">${blogUpdated} ago</p>
                </div>
              </div>
            </div>

            <div class="mt-3">
              <p class="text-muted mb-0"><a href="${commentSlug}"><strong>${commentTitle}</strong></a></p>
              <p class="text-muted mb-0">${blogContent}</p>
            </div>


          </div>

            <div class="mt-3">
              <div class="d-flex flex-row align-items-center">
                <div class="avatar mr-3"><img class="avatar-img" src="${likeImage}"
                                              alt="avatar">
                </div>
                <div>
                ${like_dislike}
                </div>
              </div>
            </div>
      </section>
  `;
  }

  return contentType
}
