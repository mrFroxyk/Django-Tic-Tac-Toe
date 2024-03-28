// GameStatusContext.js
import React, { createContext, useContext, useState } from 'react';

const GameStatusContext = createContext();

export const GameStatusProvider = ({ children }) => {
  const [gameStatus, setGameStatus] = useState('X is moving');

  return (
    <GameStatusContext.Provider value={{ gameStatus, setGameStatus }}>
      {children}
    </GameStatusContext.Provider>
  );
};

export const useGameStatus = () => useContext(GameStatusContext);
