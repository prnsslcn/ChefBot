import React, { useState } from 'react';
import { useChat } from "../context/ChatContext"; 

export const UserInput = () => {
  const [userInput, setUserInput] = useState('');
  const { setMessages, setCallResponse, setAllMessages } = useChat(); 

  const handleInputChange = (e) => {
    setUserInput(e.target.value);
  };

  const handleSubmit = async () => {
    if (userInput.trim() !== '') {
      setMessages((prevMessages) => [...prevMessages, userInput]);
      setAllMessages((prevMessages) => [...prevMessages, userInput]);
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
  
  return (
    <div className="bg-white p-6 relative">
      <input
        type="text"
        placeholder="만들고 싶은 요리를 입력해주세요"
        className="input input-xl w-full pr-28 focus:outline-none"
        value={userInput}
        onChange={handleInputChange}  
        onKeyDown={handleKeyDown}  
      />
      <button 
      className="btn absolute right-9 top-1/2 transform -translate-y-1/2"
      onClick={handleSubmit}
      >
        전송
        <svg
          width="24"
          height="24"
          viewBox="0 0 48 48"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M44 4L22 26M44 4L30 44L22 26M44 4L4 18L22 26"
            stroke="#1E1E1E"
            strokeWidth="4"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </button>
    </div>
  );
};