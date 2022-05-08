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
    followers += followerListFunc(
      followerList[i].subscriber.image, followerList[i].subscriber.full_name, followerList[i].date);
  })
  $('#followerContainer').append(followers);
  $('.container').attr('data', data.next);
  requestedNewPageFollower = false;
}

function followerListFunc(authorImage, authorFullName, followerUpdated,) {
  let follower = `
        <section class="py-4">
            <div class="mb-4 py-4">
              <div class="d-flex justify-content-between align-items-center">
                <div class="d-flex flex-row align-items-center">
                  <div class="avatar mr-3"><img class="avatar-img" src="${authorImage}"
                                                alt="avatar">
                  </div>
                  <div>
                    <h2 class="h6 mb-0">${authorFullName}</h2>
                    <p class="small text-muted mb-0">${followerUpdated} ago</p>
                  </div>
                </div>
              </div>
              <div class="mt-3">
                <p class="text-muted mb-0">Subscribed to you</p>
              </div>
            </div>
        </section>
  `;
  return follower;
}
