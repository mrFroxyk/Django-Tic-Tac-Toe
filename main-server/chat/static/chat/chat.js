const scrollableContent = document.querySelector('.chat__scrollable');
const messageInput = document.querySelector('.chat__input')
const sendButton = document.querySelector('.chat__seng-ico')
sendButton.addEventListener('click', sendMessage)

const chat_socket = new WebSocket('ws://' + window.location.host + '/chat');
chat_socket.onmessage = function (event) {
    try {
        const data = JSON.parse(event.data)
        if (data.type === 'websocket.message') {
            console.log('Message:', data.message);
            renderMessage( data.message)
        }
    } catch (e) {
        console.log('Error:', e.message);
    }
};

function sendMessage() {
    if (messageInput.value.trim() !== '') {
        chat_socket.send(JSON.stringify(
            {
                type: 'message',
                message: messageInput.value,
            }
        ))
        messageInput.value = '';
    }
}

function renderMessage(textContent) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    messageDiv.textContent = textContent;
    scrollableContent.appendChild(messageDiv);
    scrollableContent.scrollTop = scrollableContent.scrollHeight;
}