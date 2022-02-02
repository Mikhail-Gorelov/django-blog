$(function () {
  $('.icon-badge').attr('data', 0);
  $('.icon-badge').text($('.icon-badge').attr('data'));
});
const ws_scheme = window.location.protocol === "https:" ? "wss://" : "ws://";
let chat_host = 'localhost:8010'
chat = new ReconnectingWebSocket(
  ws_scheme
  + chat_host
  + '/ws/chat/'
);
chat.onclose = closeChat;
chat.onmessage = messageInChat;

function closeChat(e) {
  console.error('Chat socket closed unexpectedly');
}

function messageInChat(e) {
  const data = JSON.parse(e.data);
  if (data.command == "new_message") {
    console.log('new message!', data);
    let temp = Number($('.icon-badge').attr('data'));
    $('.icon-badge').attr('data', temp + 1);
    $('.icon-badge').text("");
    $('.icon-badge').text($('.icon-badge').attr('data'));
  }
}
