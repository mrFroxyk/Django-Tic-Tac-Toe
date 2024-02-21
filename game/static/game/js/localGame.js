// create tic tac toe board
const container = document.getElementById('game-board')
for (let i = 0; i < 9; i++) {
    const square = document.createElement('div')
    square.addEventListener('click', handleClick)
    square.classList.add('game-board__squared')
    square.id = `${i}`
    container.appendChild(square)
}