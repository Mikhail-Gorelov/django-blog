$(function () {
  $('#chat-connect').click(ChatConnect);
});
console.log("Hello world!");

function ChatConnect(e) {
  let href = $('#chat-connect').data("href");
  let jwt = localStorage.getItem('access_token');
  let user_id = $('#chat-connect').data("id");
  // TODO: починить user_id, отправка письма с фронтом
  let url = href + "?auth=" + jwt + "&user_id=" + user_id;

  window.open(url,"_blank").focus();
}
