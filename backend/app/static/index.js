document.querySelector('#chat-name-input').focus();
document.querySelector('#chat-name-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-name-submit').click();
    }
};

document.querySelector('#chat-name-submit').onclick = function(e) {
    var chatName = document.querySelector('#chat-name-input').value;
    window.location.pathname = '/chat/' + chatName + '/';
};