import React from "react";
import { Link } from "react-router-dom";
import '../styles/Navbar.css'
import '../img/logo.png'

const Navbar = function navBar() {
    return (
        <nav className="nav">
            <img src="./img/logo.png" alt="" className="nav__logo" />
            <ul className="nav__bar">
                <li className="nav__menu-item">
                    <Link to="/1" >Local game</Link>
                </li>
                <li className="nav__menu-item">
                    <Link to="/1">Search game</Link>
                </li>
                <li className="nav__menu-item">
                    <Link to="/2">Playing with a friend</Link>
                </li>
            </ul>
            <div className="user">
                <div className="user__ava">

                </div>
                <div className="user__nickname">
                    Admin
                </div>
            </div>
        </nav>
    )
}

export default Navbar;