const chatLog = document.querySelector('#chat-log')
const chatName = JSON.parse(document.getElementById('chat-name').textContent);
const enterCode = 12;

if (chatLog.childNodes.length <= 1) {
    const emptyText = document.createElement('h3')
    emptyText.id = 'emptyText'
    emptyText.innerText = 'Нет сообщений'
    emptyText.className = 'emptyText'
    chatLog.appendChild(emptyText)
}

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + chatName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const messageElement = document.createElement('div')
    const userId = data['user_id']
    const loggedInUserId = JSON.parse(document.getElementById('user_id').textContent)
    console.log(loggedInUserId)
    messageElement.innerText = data.message
    
    if (userId === loggedInUserId) {
        messageElement.classList.add('message', 'sender')
    } else {
        messageElement.classList.add('message', 'receiver')
    }

    chatLog.appendChild(messageElement)

    if (document.querySelector('#emptyText')) {
        document.querySelector('#emptyText').remove()
    }
};

chatSocket.onclose = function(e) {
    console.error('Вебсокет закрылся в связи с ошибкой');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === enterCode) {
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({ 'message': message}));
    messageInputDom.value = '';
};