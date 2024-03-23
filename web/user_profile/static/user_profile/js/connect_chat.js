$(function () {
  $('#chat-connect').click(ChatConnect);
});

function ChatConnect(e) {
  let href = $('#chat-connect').data("href");
  let jwt = localStorage.getItem('access_token');
  let user_id = $('#chat-connect').data("id");
  // NOTE: fix user_id, send email with frontend stuff
  let url = href + "?auth=" + jwt + "&user_id=" + user_id;

  window.open(url,"_blank").focus();
}
