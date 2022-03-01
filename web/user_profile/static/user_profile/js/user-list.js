$(function () {
  $('.send-message').click(sendMessage);
  let panels = $('.user-infos');  // unique
  let panelsButton = $('.dropdown-user');
  panels.hide();

  //Click dropdown
  panelsButton.click(function () {
    //get data-for attribute
    let dataFor = $(this).attr('data-for');  // unique
    let idFor = $(dataFor);

    //current button
    let currentButton = $(this);
    idFor.slideToggle(400, function () {
      //Completed slidetoggle
      if (idFor.is(':visible')) {
        currentButton.html('<i class="icon-chevron-up text-muted"></i>');
      } else {
        currentButton.html('<i class="icon-chevron-down text-muted"></i>');
      }
    })
  });


  $('[data-toggle="tooltip"]').tooltip();

  $('button').click(function (e) {
    e.preventDefault();
    alert("This is a demo.\n :-)");
  });
});

function sendMessage() {
  let user_id = $(this).data("id");
  let href = $('.send-message').data("href");
  let jwt = localStorage.getItem('access_token');

  let url = href + "?auth=" + jwt + "&user_id=" + user_id;

  window.open(url, "_blank").focus();
}
