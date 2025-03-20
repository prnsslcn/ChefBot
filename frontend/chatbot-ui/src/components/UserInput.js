import { useState } from "react";
import { useChat } from "../context/ChatContext";

export const UserInput = () => {
  const [userInput, setUserInput] = useState("");
  const [showCategoryPopup, setShowCategoryPopup] = useState(false);
  const [isFadingOut, setIsFadingOut] = useState(false);
  const { isAiResponding, setMessages, setAllMessages, setCallResponse, optionCheck, setOptionCheck } = useChat();

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

  const handleCheckboxChange = (option) => {
    if (option === "전체 🍽️") {
      setOptionCheck(""); // 서버에 category는 빈 값으로 전달됨
    } else {
      setOptionCheck(option);
    }
    handleCloseCategoryPopup(); // 팝업 닫기
  };  

  const handleCloseCategoryPopup = () => {
    setIsFadingOut(true);
    setTimeout(() => {
      setShowCategoryPopup(false);
      setIsFadingOut(false);
    }, 1000); // fadeout 애니메이션 시간과 일치시켜야 함
  };  
  
  const categoryOptions = ["전체 🍽️", "한식 🍚", "중식 🍲", "일식 🍣", "양식 🍝"];

  return (
    <div className="p-4 border-t border-gray-200 bg-white flex items-center gap-3">
      {/* 🍱 카테고리 버튼 */}
      <div className="relative">
        <button
          onClick={() => setShowCategoryPopup(!showCategoryPopup)}
          className="w-12 h-12 bg-emerald-500 hover:bg-emerald-700 rounded-full flex items-center justify-center text-white shadow-lg"
        >
          <img
            src="https://img.icons8.com/fluency-systems-filled/96/ffffff/rice-bowl.png"
            alt="Category"
            className="w-6 h-6"
          />
        </button>

        {/* 📂 카테고리 팝업 */}
        {showCategoryPopup && (
          <div className={`absolute bottom-20 left-0 bg-white border border-gray-300 rounded-2xl shadow-xl p-4 z-50 w-60
            ${isFadingOut ? "animate-fadeoutCategory" : "animate-fadeinCategory"}`}
          >
            <p className="text-base font-bold mb-4 text-gray-800 text-center">🍱 카테고리 선택</p>
            <ul className="space-y-2">
              {categoryOptions.map((option) => {
                const isSelected = optionCheck === option;
                return (
                  <li key={option}>
                    <label
                      className={`flex items-center space-x-2 cursor-pointer text-sm px-2 py-2 rounded-lg transition-colors duration-200
                        ${isSelected ? "bg-emerald-100 border border-emerald-500 font-semibold text-emerald-700" : "hover:bg-gray-100"}
                      `}
                    >
                      <input
                        type="radio"
                        name="category"
                        value={option}
                        checked={isSelected}
                        onChange={() => {
                          setOptionCheck(option);
                          handleCloseCategoryPopup();
                        }}
                        className="hidden"
                      />
                      <span>{option}</span>
                    </label>
                  </li>
                );
              })}
            </ul>
          </div>
        )}
      </div>
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
