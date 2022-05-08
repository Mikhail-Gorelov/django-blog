$(function () {
  getArticleList();
});
$.fn.scrollBottom = function () {
  return $(document).height() - this.scrollTop() - this.height();
};
let requestedNewPageArticle = false;
$(document).scroll(function () {
  if ($(this).height() - $(this).scrollTop() < 1000  && !requestedNewPageArticle) {
    if ($('.container').attr('data')) {
      requestedNewPageArticle = true;
      getArticleList($('.container').attr('data'));
    }
  }
});

function getArticleList(url = null) {
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
      articleListRender(data);
    },
  })
}

function articleListRender(data) {
  let articleList = data.results;
  $(".container").attr("data-href", data.next);

  let articles = ``;
  $.each(articleList, function (i) {
    articles += articleListFunc(
      articleList[i].author.image, articleList[i].author.full_name, articleList[i].updated, articleList[i].image,
      articleList[i].title, articleList[i].content,);
  })
  $('#articleContainer').append(articles);
  $('.container').attr('data', data.next);
  requestedNewPageArticle = false;
}

function articleListFunc(authorImage, authorFullName, articleUpdated, articleImage, articleTitle, articleContent) {
  let article = `
        <section class="py-4">
            <div class="mb-4 py-4">
              <div class="d-flex justify-content-between align-items-center">
                <div class="d-flex flex-row align-items-center">
                  <div class="avatar mr-3"><img class="avatar-img" src="${authorImage}"
                                                alt="avatar">
                  </div>
                  <div>
                    <h2 class="h6 mb-0">${authorFullName}</h2>
                    <p class="small text-muted mb-0">${articleUpdated} ago</p>
                  </div>
                </div>
              </div>
              <img class="rounded w-100 mt-3" src="${articleImage}" alt="feed">
              <div class="mt-3">
                <h4 class="h5"> ${articleTitle} </h4>
                <p class="text-muted mb-0">${articleContent}</p>
              </div>
            </div>
        </section>
  `;
  return article;
}
