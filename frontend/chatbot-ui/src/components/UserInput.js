import React, { useState } from 'react';
import { useChat } from "../context/ChatContext"; 

export const UserInput = () => {
  const [userInput, setUserInput] = useState('');
  const { setMessages, setCallResponse } = useChat(); 

  const handleInputChange = (e) => {
    setUserInput(e.target.value);
  };

  const handleSubmit = async () => {
    if (userInput.trim() !== '') {
      setMessages((prevMessages) => [...prevMessages, userInput]);
      setCallResponse(true);
      setUserInput(''); 
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSubmit();
    }
  };
  // fixed bottom-0 left-0 w-full z-10
  return (
    <div className="bg-white p-4 ">
      <input
        type="text"
        placeholder="만들고 싶은 요리를 입력해주세요"
        className="input input-xl w-full focus:outline-none"
        value={userInput}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
      />
      <button
        className="btn btn-outline mt-4"
        onClick={handleSubmit}
      >
        보내기
      </button>
    </div>
  );
};