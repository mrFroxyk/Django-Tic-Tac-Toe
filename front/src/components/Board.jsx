import { useState } from 'react'
import '../styles/game.css'
import '../styles/LocalGame.css'
import { useGameStatus } from '../context/GameStatusContext'

const LocalGame = function () {

    return (
        <div className="content">
            <GameStatus />
            <Board />
        </div>
    )
}

const GameStatus = () => {
    const { gameStatus } = useGameStatus();
    function handleReload() {
        window.location.reload();
    };

    return (
        <div className='game-status' onClick={handleReload}>
            Статус игры: {gameStatus}
        </div>
    );
};

const Board = function () {

    // eslint-disable-next-line
    const { gameStatus, setGameStatus } = useGameStatus();
    const [board, setBoard] = useState(Array(9).fill(""))
    const [isCanPlay, setIsCanPlay] = useState(true)
    let [currentMove, setCurrentMove] = useState(true)
    function handleClick(squaredId) {
        console.log(squaredId, board[squaredId])
        if (board[squaredId] === "" && isCanPlay) {
            let currentBoard = board.slice()
            currentBoard[squaredId] = (currentMove ? "X" : "O")
            setBoard(currentBoard)
            setCurrentMove(!currentMove)
            setGameStatus(`${currentMove ? "O" : "X"} is moving`)
            calculateWinner(currentBoard)
        }
    }
    return (
        <div className="game-board" id="game-board">
            <Squared handleClick={handleClick} id={0} children={board[0]} />
            <Squared handleClick={handleClick} id={1} children={board[1]} />
            <Squared handleClick={handleClick} id={2} children={board[2]} />
            <Squared handleClick={handleClick} id={3} children={board[3]} />
            <Squared handleClick={handleClick} id={4} children={board[4]} />
            <Squared handleClick={handleClick} id={5} children={board[5]} />
            <Squared handleClick={handleClick} id={6} children={board[6]} />
            <Squared handleClick={handleClick} id={7} children={board[7]} />
            <Squared handleClick={handleClick} id={8} children={board[8]} />
        </div>
    )

    function calculateWinner(currentSquares) {
        const lines = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ];
        let isAllSquaresFull = true
        lines.forEach((item) => {
            const [a, b, c] = item
            if (currentSquares[a] === currentSquares[b] && currentSquares[b] === currentSquares[c] && currentSquares[a] !== "") {
                setGameStatus("Player " + (currentMove ? "X" : "O") + ' is win')
                setIsCanPlay(false)
            }
            else if (!(currentSquares[a] !== "" && currentSquares[b] !== "" && currentSquares[c] !== "")) {
                isAllSquaresFull = false
            }
        })
        if (isAllSquaresFull) {
            setGameStatus("Nobody win! The game end")
            setIsCanPlay(false)
        }
    }
}

function Squared({ id, handleClick, children }) {

    return (
        <div className="game-board__squared" id={id} onClick={() => handleClick(id)}>
            {children}
        </div>
    )
}
export default LocalGame