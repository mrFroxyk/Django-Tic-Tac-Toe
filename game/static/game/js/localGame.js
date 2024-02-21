// create tic tac toe board
const container = document.getElementById('game-board')
const gameStatus = document.querySelector('.game-status')
let board = new Array(9).fill('')
for (let i = 0; i < 9; i++) {
    const square = document.createElement('div')
    square.addEventListener('click', handleClick)
    square.classList.add('game-board__squared')
    square.id = `${i}`
    container.appendChild(square)
    gameStatus.textContent = `Player X is moving`
}


let currentMove = 'X'
let isCanMove = true

function handleClick(event) {
    let moveId = event.target.id
    if (board[moveId] === '' && isCanMove) {
        board[moveId] = currentMove
        currentMove = (currentMove === 'X' ? 'O' : 'X')
        renderValue(board)
        gameStatus.textContent = `Player ${currentMove} is moving`
        checkWinners()
    }
}


const squares = document.querySelectorAll('.game-board__squared')

function renderValue(board) {
    for (let i = 0; i < 9; i++) {
        squares[i].textContent = board[i]
    }
}


const winLineId = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


function checkWinners() {
    winLineId.forEach((element) => {
        const [i1, i2, i3] = element
        if (board[i1] === board[i2] && board[i2] === board[i3] && board[i1] !== '') {
            isCanMove = false
            gameStatus.textContent = `Player ${currentMove} win. Congratulation!!!\nCLICK TO REMATCH`
            gameStatus.addEventListener('click', () => {
                // console.log(location.protocol + '//' + location.host + '/game/local-game')
                // window.location.href = "https://www.google.com";
                window.location.href = location.origin + '/game/local-game'
            })
        }
    })
}