// TODO: NEED TO FINISH THIS JS FILE
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

function followerListFunc(authorImage, authorFullName, blogUpdated, blogImage, blogTitle, blogContent, likeImage,
                          likeAuthorFullName, vote) {
  let like = `
        <section class="py-4">
        {% for like in likes %}
          <div class="mb-4 py-4">
            <div class="d-flex justify-content-between align-items-center">
              <div class="d-flex flex-row align-items-center">
                <div class="avatar mr-3"><img class="avatar-img" src="{{ like.content_type.author.image }}"
                                              alt="avatar">
                </div>
                <div>
                  <h2 class="h6 mb-0">{{ like.content_type.author.full_name }}</h2>
                  <p class="small text-muted mb-0">{{ like.content_type.updated }} ago</p>
                </div>
              </div>
            </div>
            <img class="rounded w-100 mt-3" src="{{ like.content_type.image }}" alt="feed">
            <div class="mt-3">
              <h4 class="h5"> {{ like.content_type.title }} </h4>
              <p class="text-muted mb-0">{{ like.content_type.content|safe }}</p>
            </div>
            <div class="mt-3">
              <div class="d-flex flex-row align-items-center">
                <div class="avatar mr-3"><img class="avatar-img" src="{{ like.user.image }}"
                                              alt="avatar">
                </div>
                <div>
                  {% if like.vote == 1 %}
                    <h2 class="h6 mb-0">{{ like.content_type.author.full_name }}</h2>
                    <p class="small text-muted mb-0">Liked this post</p>
                  {% endif %}
                  {% if like.vote == 0 %}
                    <h2 class="h6 mb-0">{{ like.content_type.author.full_name }}</h2>
                    <p class="small text-muted mb-0">Disliked this post</p>
                  {% endif %}
                </div>
              </div>
            </div>
          </div>
        {% endfor %}
      </section>
  `;
  return like;
}
