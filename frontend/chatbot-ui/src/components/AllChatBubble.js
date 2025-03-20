import { useEffect, useRef, useState, useMemo } from "react";
import { useChat } from "../context/ChatContext";
import { LoadingSpinner } from "./LoadingSpinner";

const AllChatBubble = () => {
  const {
    allMessages,
    setAiResponse,
    setMessages,
    setAllMessages,
    callResponse,
    setStepMode,
  } = useChat();
  const [currentStep, setCurrentStep] = useState(0);
  const [showSteps, setShowSteps] = useState(false);
  const chatContainerRef = useRef(null);
  const [showLoading, setShowLoading] = useState(false);

  useEffect(() => {
    if (callResponse) {
      setShowLoading(true);
    } else {
      // 로딩 끝날 때는 0.4초 후 제거 (애니메이션 시간 맞춰서)
      const timeout = setTimeout(() => setShowLoading(false), 400);
      return () => clearTimeout(timeout);
    }
  }, [callResponse]);  

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTo({
        top: chatContainerRef.current.scrollHeight,
        behavior: 'smooth',
      });
      
    }
  }, [allMessages, currentStep]);

  const handleReTry = () => {
    setAiResponse([]);
    setMessages([]);
    setAllMessages(["어떤 요리를 만들고 싶으세요?"]);
    setShowSteps(false);
    setStepMode(false);
  };

  const handleNextStep = (steps) => {
    if (currentStep < steps.length - 1) {
      setCurrentStep((prev) => prev + 1);
    } else {
      setShowSteps(false);
      setCurrentStep(0);
    }
  };

  const renderedMessages = useMemo(
    () =>
      allMessages.map((message, index) => {
        if (typeof message === "string") {
          const isUser = message !== "어떤 요리를 만들고 싶으세요?";
          return (
            <div
              key={index}
              className={`chat-message ${isUser ? "text-right" : "text-left"} mb-2 animate-fadein`}>
              <div
                className={`inline-block px-4 py-2 rounded-xl max-w-[70%] text-base ${
                  isUser ? "bg-sky-500 text-white ml-auto" : "bg-neutral-100 text-black mr-auto"
                } shadow`}>
                {message}
              </div>
            </div>
          );
        }

        if (typeof message === "object" && message?.content) {
          return (
            <div key={index} className="chat-message text-left mb-2 animate-fadein">
              
                {message.type === "text" ? (
                  <div className="inline-block px-4 py-2 rounded-xl bg-neutral-100 text-black max-w-[70%] shadow text-base">{message.content}</div>
                ) : (
                  <img src={message.content} alt="요리 이미지" className="w-full max-w-80 h-80 rounded-lg object-cover animate-fadein" />
                )}
              </div>
            
          );
        }
        return null;
      }),
    [allMessages]
  );

  return (
    <div className="flex-1 overflow-y-auto p-4 scroll-smooth scrollbar-hidden" ref={chatContainerRef}>
      {renderedMessages}
      {showLoading && (
        <div className={`${!callResponse ? "animate-fadeout" : ""}`}>
          <LoadingSpinner />
        </div>
      )}

      {allMessages.some((msg) => msg?.type === "text" && msg.content?.includes("을 만들고 싶다면")) && (
        <div className="flex flex-col items-center my-6 animate-fadein">
          {!showSteps ? (
            <button className="bg-sky-500 hover:bg-sky-700 text-white text-lg px-6 py-3 rounded-lg shadow" onClick={() => setShowSteps(true)}>
              시작
            </button>
          ) : (
            <div className="w-full mt-4">
              <ul className="space-y-2 text-left text-base">
                {allMessages
                  .find((msg) => msg?.recipe?.steps)
                  ?.recipe?.steps?.slice(0, currentStep + 1)
                  .map((step, idx) => (
                    <li key={idx} className="p-3 bg-sky-100 rounded-lg shadow animate-fadein">{step}</li>
                  ))}
              </ul>
              <div className="flex justify-center">
                <button
                  className={`mt-4 px-6 py-3 rounded-lg text-white ${
                    currentStep < (allMessages.find((msg) => msg.recipe?.steps)?.recipe?.steps.length || 0) - 1
                      ? "bg-sky-500 hover:bg-sky-700"
                      : "bg-red-500 hover:bg-red-700"
                  }`}
                  onClick={() => {
                    const steps = allMessages.find((msg) => msg.recipe?.steps)?.recipe?.steps || [];
                    currentStep >= steps.length - 1 ? handleReTry() : handleNextStep(steps);
                  }}
                >
                  {currentStep < (allMessages.find((msg) => msg.recipe?.steps)?.recipe?.steps.length || 0) - 1
                    ? "다음"
                    : "다시 시작"}
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AllChatBubble;
