import React from "react";
import '../styles/App.css'
import { useState } from "react";

const Counter = function () {
    const [likes, setLikes] = useState(0);

    function up() {
        setLikes(likes + 1)
    }
    function down() {
        setLikes(likes - 1)
    }
    return (
        <div className="App">
            <div className="Likes">
                likes: {likes}
            </div>
            <button onClick={up}>UP</button>
            <button onClick={down}>DOWN</button>
        </div>
    );
}

export default Counter;