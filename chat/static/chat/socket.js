// const socket = new WebSocket('ws://127.0.0.1:8000/online');
const socket = new WebSocket('ws:/192.168.3.2:8000/online');
socket.onopen = function (e) {
    socket.send(JSON.stringify({
        type: 'handshake',
        message: 'Hello from Js client'
    }));
};

socket.onmessage = function (event) {
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
        socket.send(JSON.stringify({
            type: 'message',
            message: messageInput.value,
        }))
        messageInput.value = '';
        // const messageDiv = document.createElement('div');
        // messageDiv.className = 'message';
        // messageDiv.textContent = messageInput.value;
        //
        // chat.appendChild(messageDiv);
        //
        // // Очищаем поле ввода
        // messageInput.value = '';
        //
        // // Прокручиваем чат вниз, чтобы видеть последнее сообщение
        // chat.scrollTop = chat.scrollHeight;
    }
}

