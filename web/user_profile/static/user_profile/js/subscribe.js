let subButton = document.querySelector('.subscribe-button');
let apiHref = subButton.dataset.href;
let userId = subButton.dataset.user;
let count = subButton.dataset.count;
let hasSubscribed = subButton.dataset.subscribed;
let subbedClass = 'subbed';

$(function () {
  console.log(typeof hasSubscribed);
  if (hasSubscribed === "True") {
    subButton.classList.add(subbedClass);
    subButton.querySelector('.subscribe-text').innerHTML = 'Subscribed';
  }
  if (count === "") {
    subButton.dataset.count = 0;
  }
});


subButton.addEventListener('click', function (e) {
  toggleSubbed();
  follow();
  e.preventDefault();
});


function follow() {
  $.ajax({
    url: apiHref,
    type: "POST",
    dataType: 'json',
    data: {
      "to_user": userId,
    },
    success: function (data) {
      subButton.dataset.count = data["count"];
    },
  })
}

function toggleSubbed() {
  let text;

  if (subButton.classList.contains(subbedClass)) {
    subButton.classList.remove(subbedClass);
    text = 'Subscribe';
  } else {
    subButton.classList.add(subbedClass);
    text = 'Subscribed';
  }

  subButton.querySelector('.subscribe-text').innerHTML = text;
}

if ('alert' == '') {
  window.setInterval(toggleSubbed, 1000);
}
