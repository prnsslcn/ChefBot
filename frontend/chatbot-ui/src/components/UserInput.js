import React, { useState } from "react";
import { useChat } from "../context/ChatContext";
import { postQuery } from "../api/getQuery";

export const UserInput = () => {
  const [userInput, setUserInput] = useState("");
  const { isAiResponding,setMessages, setCallResponse, setAllMessages, optionCheck, setOptionCheck, setAiResponse } = useChat();


  const handleInputChange = (e) => {
    setUserInput(e.target.value);
  };

  const handleCheckboxChange = (selectedCategory) => {
    setOptionCheck(selectedCategory);
  };

  const category = ["한식", "일식", "중식", "양식"];

  const handleSubmit = async () => {
    if (!optionCheck) {
      const noCategoryMessage = {
        type: "text",
        content: "🚨 카테고리를 선택해주세요.",
      };
      setMessages((prev) => [...prev, noCategoryMessage]);
      setAllMessages((prev) => [...prev, noCategoryMessage]);
      return;
    }

    if (userInput.trim() !== "" && !isAiResponding) {
      setMessages((prevMessages) => [...prevMessages, userInput]);
      setAllMessages((prevMessages) => [...prevMessages, userInput]);
      setCallResponse(true);
      setUserInput("");

      try {
        const response = await postQuery(userInput, optionCheck);
        console.log(response);
      } catch (err) {
        console.log(err);
      }
    }
  };

  const handleKeyUp = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="bg-white p-6 relative rounded-b-xl border-b border-l border-r border-stone-300">
      <div className="font-semibold mb-2 text-lime-950">카테고리(필수)</div>
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
          onKeyUp={handleKeyUp}
        />
        <button
          className="btn absolute right-5 top-1/2 transform -translate-y-1/2"
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
