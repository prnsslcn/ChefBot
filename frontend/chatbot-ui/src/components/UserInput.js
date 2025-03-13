import React, { useState } from 'react';

export const UserInput = ({ onSendMessage }) => {
    
    const [userInput, setUserInput] = useState('');
  
    const handleInputChange = (e) => {
      setUserInput(e.target.value);
    };
  
    const handleSubmit = () => {
      if (userInput.trim() !== '') {
        onSendMessage(userInput);  
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
      <div className="bg-white p-4">
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