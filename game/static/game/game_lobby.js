const game_socket = new WebSocket('ws://127.0.0.1:8000/game_lobby');
// const game_socket = new WebSocket('ws://192.168.3.2:8000/game_lobby');
// const game_socket = new WebSocket('ws://10.30.225.191:8000/game_lobby');

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

document.addEventListener('DOMContentLoaded', function () {
    const url_button = document.querySelector('.copywriter_url')
    const green_message = document.querySelector('.copywriter_alright-window')
    green_message.style.opacity = 0
    console.log(url_button)
    let isCopied = false
    url_button.addEventListener('click', () => {
        console.log("fff")
        navigator.clipboard.writeText(url_button.textContent);
        if (!isCopied) {
            green_message.style.opacity = 1
            isCopied = true
            setTimeout(() => {
                isCopied = false
                green_message.style.opacity = 0
            }, 4000)
        }
    })
});





