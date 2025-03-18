import React, { useState } from "react";
import { useChat } from "../context/ChatContext";

export const UserInput = () => {
  const [userInput, setUserInput] = useState("");
  const { isAiResponding,setMessages, setCallResponse, setAllMessages, optionCheck, setOptionCheck } = useChat();


  const handleInputChange = (e) => {
    setUserInput(e.target.value);
  };

  const handleCheckboxChange = (selectedCategory) => {
    setOptionCheck(selectedCategory);
  };

  const category = ["한식", "일식", "중식", "양식"];

  const handleSubmit = async () => {
    if (userInput.trim() !== "" && !isAiResponding) {
      setMessages((prevMessages) => [...prevMessages, userInput]);
      setAllMessages((prevMessages) => [...prevMessages, userInput]);
      setCallResponse(true);
      setUserInput("");
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="flex space-x-4 mb-4">
        {category.map((category, idx) => (
          <label key={idx} className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={optionCheck === category}
              onChange={() => handleCheckboxChange(category)}
              className="checkbox checkbox-primary"
            />
            <span>{category}</span>
          </label>
        ))}
      </div>

      <div className="relative flex items-center">
        <input
          type="text"
          placeholder="만들고 싶은 요리를 입력해주세요"
          className="input input-xl w-full pr-28 p-3 border border-gray-300 rounded-lg focus:outline-none"
          value={userInput}
          onChange={handleInputChange}
          onKeyUp={handleKeyDown}
        />
        <button
          className="btn absolute right-9 top-1/2 transform -translate-y-1/2"
          onClick={handleSubmit}
          disabled={isAiResponding}
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
    </div>
  );
};
