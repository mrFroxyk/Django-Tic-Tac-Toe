import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import { GameStatusProvider } from "./context/GameStatusContext";
import LocalGame from "./components/Board";
import PageTwo from "./components/pagaTwo";
import Navbar from "./components/Navbar";

import './styles/style.css'


function App() {
    return (
        <div>
            <GameStatusProvider>
                <BrowserRouter>
                    <Navbar />
                    <Routes>
                        <Route path="/1" element={<LocalGame />} />
                        <Route path="/2" element={<PageTwo />} />
                    </Routes>
                </BrowserRouter>
            </GameStatusProvider>
        </div>
    )
}

export default App;
