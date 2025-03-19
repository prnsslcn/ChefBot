import React, { useState } from "react";
import { useChat } from "../context/ChatContext";
import { postQuery } from "../api/getQuery";

export const UserInput = () => {
  const [userInput, setUserInput] = useState("");
  const { setMessages, setCallResponse, setAllMessages, setAiResponse } = useChat();

  const handleInputChange = (e) => {
    setUserInput(e.target.value);
  };

  const handleSubmit = async () => {
    if (userInput.trim() !== "") {
      setMessages((prevMessages) => [...prevMessages, userInput]);
      setAllMessages((prevMessages) => [...prevMessages, userInput]);
      setCallResponse(true);

      try {
        const response = await postQuery(userInput);

        const newMessages = [
          {
            type: "text",
            content: `${response.recipe.title}`,
          },
          {
            type: "text",
            content: `📌 재료 : ${response.recipe.ingredients.join(", ")}`,
          },
          {
            type: "image",
            content: response.image_url,
          },
          {
            type: "text",
            content: `${response.recipe.title}을 만들고 싶다면 "시작" 버튼을 눌러주세요`,
          },
        ];

        for (const msg of newMessages) {
          await new Promise((res) => setTimeout(res, 1000));
          setAiResponse((prev) => [...prev, msg]);
          setAllMessages((prev) => [...prev, msg]);
        }

        // 레시피 조리 단계를 마지막에 추가
        setAllMessages((prev) => [
          ...prev,
          { recipe: { steps: response.recipe.steps } },
        ]);
      } catch (error) {
        console.error("AI 요청 실패:", error);
      }

      setUserInput("");
      setCallResponse(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
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
        onKeyUp={handleKeyDown}
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
