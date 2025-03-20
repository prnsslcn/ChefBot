import { useState } from "react";
import { useChat } from "../context/ChatContext";

export const UserInput = () => {
  const [userInput, setUserInput] = useState("");
  const { isAiResponding, setMessages, setAllMessages, setCallResponse } = useChat();

  const handleSubmit = () => {
    if (!userInput.trim()) return;
    setMessages((prev) => [...prev, userInput]);
    setAllMessages((prev) => [...prev, userInput]);
    setCallResponse(true);
    setUserInput("");
  };

  const handleKeyUp = (e) => {
    if (e.key === "Enter") handleSubmit();
  };

  return (
    <div className="p-4 border-t border-gray-200 bg-white flex items-center gap-3">
      <button
        onClick={handleSubmit}
        disabled={isAiResponding}
        className="w-12 h-12 bg-emerald-500 hover:bg-emerald-700 rounded-full flex items-center justify-center text-white shadow-lg"
      >
        <img
          src="https://img.icons8.com/fluency-systems-filled/96/ffffff/rice-bowl.png"
          alt="Send"
          className="w-6 h-6"
        />
      </button>
      <input
        type="text"
        placeholder="만들고 싶은 요리를 입력해주세요"
        className="flex-grow border border-gray-300 rounded-full px-4 py-3 text-base focus:outline-none shadow-inner"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        onKeyUp={(e) => e.key === "Enter" && handleSubmit()}
      />
      <button
        onClick={handleSubmit}
        disabled={isAiResponding}
        className="w-12 h-12 bg-sky-500 hover:bg-sky-700 rounded-full flex items-center justify-center text-white shadow-lg"
      >
        <img
          src="https://img.icons8.com/ios-glyphs/90/ffffff/paper-plane.png"
          alt="Send"
          className="w-6 h-6"
        />
      </button>
    </div>
  );
};
