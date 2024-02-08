const chat_socket = new WebSocket('ws://127.0.0.1:8000/chat');
// const chat_socket = new WebSocket('ws://192.168.3.2:8000/chat');
// const chat_socket = new WebSocket('ws://10.30.225.191:8000/chat');
// const chat_socket = new WebSocket('ws:/192.168.3.2:8000/chat');
chat_socket.onopen = function (e) {
    chat_socket.send(JSON.stringify({
        type: 'handshake',
        message: 'Hello from Js client'
    }));
};

chat_socket.onmessage = function (event) {
    try {
        const data = JSON.parse(event.data)
        if (data.type === 'websocket.message'){
            console.log('Message:', data.message);
            renderMessage(data.message)
        }
    } catch (e) {
        console.log('Error:', e.message);
    }
};

function renderMessage(textContent){
    const chat = document.getElementById('chat');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    messageDiv.textContent = textContent;
    chat.appendChild(messageDiv);
    chat.scrollTop = chat.scrollHeight;
}
function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const chat = document.getElementById('chat');

    if (messageInput.value.trim() !== '') {
        chat_socket.send(JSON.stringify({
            type: 'message',
            message: messageInput.value,
        }))
        messageInput.value = '';
    }
}

