

const game_socket = new WebSocket('ws://127.0.0.1:8000/game_lobby');

// const socket = new WebSocket('ws:/192.168.3.2:8000/chat');
game_socket.onopen = function (e) {
    game_socket.send(JSON.stringify({
        type: 'handshake',
        message: 'Hello from Js client'
    }));
    const currentURL = window.location.href;
    const segments = currentURL.split('/');
    const room_code = segments[segments.length - 2]; //get room_code
    console.log(room_code)

    game_socket.send(JSON.stringify({
        type: 'join',
        room_code: room_code
    })) // try to join to the room by room code
};

game_socket.onmessage = function (event) {
    try {
        const data = JSON.parse(event.data)
        if (data.type === 'websocket.message') {
            console.log('Message:', data.message);
        }
        if (data.type === 'websocket.redirect') {
            game_socket.close()
            const currentURL = window.location.href;
            let segments = currentURL.split('/');
            segments[segments.length - 1] = 'game';
            const resultUrl = segments.join('/')
            console.log('redirect:', resultUrl);
            window.location.href = resultUrl;
        }
    } catch (e) {
        console.log('Error:', e.message);
    }
};





