import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Counter from "./components/counter";
import Navbar from "./components/Navbar";
import PageTwo from "./components/pagaTwo";
import './styles/style.css'

function App() {
    return (
        <div>
            <BrowserRouter>
                <Navbar />
                <Routes>
                    <Route path="/1" element={<Counter />} />
                    <Route path="/2" element={<PageTwo />} />
                </Routes>
            </BrowserRouter>
        </div>
    )
}

export default App;
