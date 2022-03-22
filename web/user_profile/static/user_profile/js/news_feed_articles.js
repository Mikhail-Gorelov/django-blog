$(function () {
  getArticleList();
});
$.fn.scrollBottom = function () {
  console.log($(document).height(), this.scrollTop(), this.height());
  return $(document).height() - this.scrollTop() - this.height();
};
let requestedNewPageArticle = false;
$('.container').scroll(function () {
  console.log($(this).prop('scrollHeight'), $(this).height(), $(this).scrollTop(), !requestedNewPage);
  if (($(this).prop('scrollHeight') - $(this).height()) <= $(this).scrollTop() && !requestedNewPage) {
    if ($(this).attr("data-href")) {
      requestedNewPageArticle = true;
      getArticleList();
    }
  }
});

function getArticleList() {
  $.ajax({
    url: $(".container").attr("data-href"),
    type: "GET",
    success: function (data) {
      articleListRender(data);
    },
  })
}

function articleListRender(data) {
  let articleList = data.results;
  $(".container").attr("data-href", data.next);

  let blockStart = `
  <div class="col-md-7">
    <div class="card">
      <div class="col-12 col-lg-7 order-lg-1">`;
  let articles = ``;
  let blockEnd = `
          </div>
      </div>
  </div>`;
  $.each(articleList, function (i) {
    articles += articleListFunc(
      articleList[i].author.image, articleList[i].author.full_name, articleList[i].updated, articleList[i].image,
      articleList[i].title, articleList[i].content,);
  })
  blockStart += articles
  blockStart += blockEnd
  $('.row').append(blockStart);
  requestedNewPage = false;
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
