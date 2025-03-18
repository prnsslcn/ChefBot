import React, { useMemo, useState, useEffect, useRef } from "react";
import { useChat } from "../context/ChatContext";

const AllChatBubble = () => {
  const { allMessages, setAiResponse, setMessages, setAllMessages } = useChat();
  const [currentStep, setCurrentStep] = useState(0);
  const [showSteps, setShowSteps] = useState(false);
  const chatContainerRef = useRef(null);

  const handleReTry = () => {
    setAiResponse([]);
    setMessages([]);
    setAllMessages(["어떤 요리를 만들고 싶으세요?"]);
    setShowSteps(false);
  };

  useEffect(() => {
    if (
      allMessages.some(
        (msg) => msg.type === "text" && msg.content.includes("을 만들고 싶다면")
      )
    ) {
      setShowSteps(false);
      setCurrentStep(0);
    }
  }, [allMessages]);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [allMessages, currentStep]);

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
        // string 메시지 처리
        if (typeof message === "string") {
          return (
            <div
              key={index}
              className={`chat ${
                message === "어떤 요리를 만들고 싶으세요?"
                  ? "chat-start"
                  : "chat-end"
              }`}
            >
              <div
                className={`chat-bubble text-xl ${
                  message === "어떤 요리를 만들고 싶으세요?"
                    ? "bg-lime-600 text-lime-50"
                    : "bg-stone-200 text-stone-900"
                }`}
              >
                {message}
              </div>
            </div>
          );
        }

        // object 메시지 처리
        if (typeof message === "object" && message !== null) {
          if (message.content) {
            return (
              <div key={index} className="chat chat-start">
                <div className="chat-bubble bg-lime-600 text-lime-50 text-xl">
                  {message.type === "text" ? (
                    <div>{message.content}</div>
                  ) : (
                    <img
                      src={message.content}
                      alt="요리 이미지"
                      className="w-full h-64 rounded-lg"
                    />
                  )}
                </div>
              </div>
            );
          }
        }
        return null;
      }),
    [allMessages, showSteps, currentStep]
  );

  return (
    <div className="bg-white w-full h-full grow p-6 flex flex-col rounded-t-xl border-t border-l border-r border-stone-300">
      <div
        ref={chatContainerRef}
        className="overflow-y-auto flex-grow max-h-[60vh] flex flex-col"
      >
        {renderedMessages}
        {/* "을 만들고 싶다면"이 포함된 메시지가 있을 때만 시작 버튼 노출 */}
        {allMessages.some(
          (msg) =>
            msg.type === "text" && msg.content.includes("을 만들고 싶다면")
        ) && (
          <div className="flex flex-col items-center my-6">
            {!showSteps ? (
              <button
                className="btn bg-amber-500 text-amber-50 w-1/3 text-2xl p-6"
                onClick={() => setShowSteps(true)}
              >
                시작
              </button>
            ) : (
              <div className="w-full flex items-center flex-col border-t border-stone-300 pt-4">
                <ul className="steps steps-vertical">
                  {allMessages
                    .find((msg) => msg.recipe?.steps)
                    ?.recipe?.steps?.slice(0, currentStep + 1)
                    .map((step, stepIndex) => (
                      <li key={stepIndex} className="step step-primary text-xl">
                        {step}
                      </li>
                    ))}
                </ul>
                <button
                  className={`btn text-xl p-6 mt-4 ${
                    currentStep <
                    (allMessages.find((msg) => msg.recipe?.steps)?.recipe?.steps
                      .length || 0) -
                      1
                      ? "bg-amber-600 text-amber-50"
                      : "bg-red-600 text-red-50"
                  }`}
                  onClick={() => {
                    if (
                      currentStep >=
                      (allMessages.find((msg) => msg.recipe?.steps)?.recipe
                        ?.steps.length || 0) -
                        1
                    ) {
                      handleReTry(); // 👉 "다시 시작"을 눌렀을 때 초기화
                    } else {
                      handleNextStep(
                        allMessages.find((msg) => msg.recipe?.steps)?.recipe
                          ?.steps || []
                      );
                    }
                  }}
                >
                  {currentStep <
                  (allMessages.find((msg) => msg.recipe?.steps)?.recipe?.steps
                    .length || 0) -
                    1
                    ? "다음"
                    : "다시 시작"}
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default AllChatBubble;
