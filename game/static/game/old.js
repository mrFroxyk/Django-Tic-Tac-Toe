const game_socket = new WebSocket('ws://127.0.0.1:8000/game');
// const socket = new WebSocket('ws:/192.168.3.2:8000/chat');
game_socket.onopen = function (e) {
    game_socket.send(JSON.stringify({
        type: 'handshake',
        message: 'Hello from Js client, wanna play!'
    })); // hello message


};

game_socket.onmessage = function (event) {
    try {
        const data = JSON.parse(event.data)
        if (data.type === 'websocket.message') {
            console.log('Message:', data.message);
            renderMessage(data.message)
        }
    } catch (e) {
        console.log('Error:', e.message);
    }
};