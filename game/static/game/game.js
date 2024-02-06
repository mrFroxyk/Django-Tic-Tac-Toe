function handleClick(event) {
    console.log(event.target.id)
    socket.send(
        JSON.stringify(
            {
                type: 'move',
                position: event.target.id,
            }
        )
    )
}

const container = document.getElementById('square-container')
for (let i = 0; i < 9; i++) {
    const square = document.createElement('div')
    square.addEventListener('click', handleClick)
    square.classList.add('square')
    square.id = `${i}`
    container.appendChild(square)
}

function renderValues(values) {
    const squares = document.querySelectorAll('.square')
    squares.forEach((square, index) => {
        square.textContent = values[index]
    })
}


const socket = new WebSocket('ws://127.0.0.1:8000/game')
// const socket = new WebSocket('ws://192.168.3.2:8000/game')
socket.onopen = function (event) {
    socket.send(
        JSON.stringify(
            {
                type: 'handshake',
                message: 'Hello from js client! (in game)'
            }
        )
    )
    const currentURL = window.location.href
    let segment = currentURL.split('/')
    const room_code = segment [segment.length - 2]
    console.log(room_code)

    socket.send(
        JSON.stringify(
            {
                type: 'join',
                room_code: room_code,
            }
        )
    )
}

socket.onmessage = function (event) {
    try {
        const data = JSON.parse(event.data)
        const border_to_render = data.border_to_render
        renderValues(border_to_render)

    } catch (e) {
        console.log(`Error ${e}`)
    }
}