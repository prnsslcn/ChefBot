import React, { useMemo, useState, useEffect } from "react";
import { useChat } from "../context/ChatContext";

const AllChatBubble = () => {
  const { allMessages } = useChat();
  const [currentStep, setCurrentStep] = useState(0);
  const [showSteps, setShowSteps] = useState(false);

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
                    ? "bg-yellow-400"
                    : "bg-sky-400"
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
                <div className="chat-bubble bg-yellow-400 text-xl">
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
    <div className="bg-white w-full p-4 flex flex-col gap-2">
      {renderedMessages}

      {/* "을 만들고 싶다면"이 포함된 메시지가 있을 때만 시작 버튼 노출 */}
      {allMessages.some(
        (msg) => msg.type === "text" && msg.content.includes("을 만들고 싶다면")
      ) && (
        <div className="flex flex-col items-center my-6">
          {!showSteps ? (
            <button
              className="btn bg-sky-400 w-1/3 text-2xl p-6"
              onClick={() => setShowSteps(true)}
            >
              시작
            </button>
          ) : (
            <div className="w-full flex flex-col items-center">
              <ul className="steps steps-vertical w-2/3">
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
                    ? "bg-emerald-400 text-emerald-900"
                    : "bg-red-400 text-white"
                }`}
                onClick={() =>
                  handleNextStep(
                    allMessages.find((msg) => msg.recipe?.steps)?.recipe
                      ?.steps || []
                  )
                }
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
  );
};

export default AllChatBubble;
