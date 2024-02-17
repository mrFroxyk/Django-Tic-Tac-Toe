const currentURL = window.location.href
let segment = currentURL.split('/')
const room_code = segment [segment.length - 2]

// from http://127.0.0.1:8000/game/8f794f32eeba8593/game get 8f794f32eeba8593
function handleClick(event) {
    socket.send(
        JSON.stringify(
            {
                type: 'move',
                room_code: room_code,
                position: event.target.id,
            }
        )
    )
}

// create tic tac toe board
const container = document.getElementById('game-board')
for (let i = 0; i < 9; i++) {
    const square = document.createElement('div')
    square.addEventListener('click', handleClick)
    square.classList.add('game-board__squared')
    square.id = `${i}`
    container.appendChild(square)
}

function renderBoardDom(values) {
    const squares = document.querySelectorAll('.game-board__squared')
    console.log(values)
    squares.forEach((square, index) => {
        square.textContent = values[index]
    })
}


const socket = new WebSocket('ws://' + window.location.host + '/game?room_code=' + room_code)

const player1_time = document.getElementById('player1_time')
const player2_time = document.getElementById('player2_time')
let currentCuratine;
let time_player1 = 0
let time_player2 = 0
const status_block = document.querySelector(".game__status")
socket.onmessage = function (event) {
    try {
        const data = JSON.parse(event.data)
        console.log(data)
        switch (data.type) {
            case 'game.move':
                const border_to_render = data.border_to_render
                renderBoardDom(border_to_render)
                status_block.textContent = data['status']
                renderTimeInDom(data)
                break;
            case 'game.end':
                let textContent = status_block.textContent;
                status_block.textContent = '';
                const button = document.createElement('button');
                button.textContent = textContent;
                button.addEventListener('click', revengeOnClick);
                status_block.appendChild(button)
                console.log('game end((')
                clearInterval(currentCuratine)
                break;
            case 'game.revenge':
                if (!isRevengeSent) {
                    console.log('получил приглашение на реванш')
                } else {
                    console.log('отправил приглос на реванш')
                }
                break;
            case 'game.redirect':
                let resultUrl = window.location.protocol + "//" + window.location.host + data.relative_url;
                console.log('redirect:', resultUrl);
                window.location.href = resultUrl;
                break;
        }
    } catch (e) {
        console.log(`Error ${e}`)
    }
}

let isRevengeSent = false

function revengeOnClick() {
    console.log('Кнопка нажата!');
    if (!isRevengeSent) {
        socket.send(JSON.stringify(
            {
                type: 'revenge_request',
                room_code: room_code
            }
        ))
    }
    isRevengeSent = true
}

function renderTimeInDom(data) {
    let current_player = data['current_player']
    let temp_time_player1 = parseInt(data['player1_time'])
    let temp_time_player2 = parseInt(data['player2_time'])
    if (Math.abs(time_player1 - temp_time_player1) > 1) {
        time_player1 = temp_time_player1
    }
    if (Math.abs(time_player2 - temp_time_player2) > 1) {
        time_player2 = temp_time_player2
    }
    player1_time.textContent = getParsedTime(time_player1)
    player2_time.textContent = getParsedTime(time_player2)
    switch (current_player) {
        case 'player1':
            --time_player1;
            if (currentCuratine) {
                clearInterval(currentCuratine)
            }
            currentCuratine = setInterval(() => {
                renderTime(player1_time, time_player1);
                --time_player1;
            }, 1000)
            player1_time.style.backgroundColor = '#9DFF09'
            player2_time.style.backgroundColor = '#D7E02A'
            break;
        case 'player2':
            --time_player2;
            if (currentCuratine) {
                clearInterval(currentCuratine)
            }
            currentCuratine = setInterval(() => {
                renderTime(player2_time, time_player2);
                --time_player2;
            }, 1000)
            player2_time.style.backgroundColor = '#9DFF09'
            player1_time.style.backgroundColor = '#D7E02A'
            break;
    }
}

function renderTime(element, startTime) {
    startTime = getParsedTime(startTime)
    element.textContent = startTime;
}

function getParsedTime(second) {
    let realMinute = ~~(second / 60);
    let realSecond = second - realMinute * 60;
    return realMinute.toString() + ": " + realSecond.toString();
}