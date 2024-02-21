const currentURL = window.location.href;
const segments = currentURL.split('/');
const room_code = segments[segments.length - 2];
//get room_code: from http://127.0.0.1:8000/game/8f794f32eeba8593/game get 8f794f32eeba8593

const game_socket = new WebSocket('ws://' + window.location.host + '/game_lobby?room_code=' + room_code);

game_socket.onmessage = function (event) {
    try {
        const data = JSON.parse(event.data)
        if (data.type === 'lobby.redirect') {
            let resultUrl = window.location.protocol + "//" + window.location.host + data.relative_url;
            console.log('redirect:', resultUrl);
            window.location.href = resultUrl;
        }
    } catch (e) {
        alert('Error:' + e.message)
    }
};

document.addEventListener('DOMContentLoaded', function () {
    // logic for copy invite url
    const url_button = document.querySelector('.copywriter_url')
    const green_message = document.querySelector('.copywriter_alright-window')
    green_message.style.opacity = 0
    console.log(url_button)
    let isCopied = false
    url_button.addEventListener('click', () => {
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





