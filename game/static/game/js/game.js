function handleClick(event) {
    socket.send(
        JSON.stringify(
            {
                type: 'move',
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

function renderValues(values) {
    const squares = document.querySelectorAll('.game-board__squared')
    console.log(values)
    squares.forEach((square, index) => {
        square.textContent = values[index]
    })
}


const socket = new WebSocket('ws://127.0.0.1:8000/game')
// const socket = new WebSocket('ws://192.168.3.2:8000/game')
// const socket = new WebSocket('ws://10.30.225.191:8000/game')
socket.onopen = function (event) {
    const currentURL = window.location.href
    let segment = currentURL.split('/')
    const room_code = segment [segment.length - 2]

    socket.send(
        JSON.stringify(
            {
                type: 'join',
                room_code: room_code,
            }
        )
    )
}

const player1_time = document.getElementById('player1_time')
const player2_time = document.getElementById('player2_time')
let currentCuratine;
let time_player1 = 0
let time_player2 = 0
socket.onmessage = function (event) {
    try {
        const data = JSON.parse(event.data)
        const border_to_render = data.border_to_render
        console.log(data)
        let temp_time_player1 = parseInt(data['player1_time'])
        let temp_time_player2 = parseInt(data['player2_time'])
        if (Math.abs(time_player1 - temp_time_player1) > 1) {
            time_player1 = temp_time_player1
        }
        if (Math.abs(time_player2 - temp_time_player2) > 1) {
            time_player2 = temp_time_player2
        }
        renderValues(border_to_render)
        let current_player = data['current_player']
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
    } catch (e) {
        console.log(`Error ${e}`)
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