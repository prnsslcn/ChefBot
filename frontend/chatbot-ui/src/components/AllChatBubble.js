import React, { useMemo, useState, useEffect, useRef } from "react";
import { useChat } from "../context/ChatContext";

const AllChatBubble = () => {
  const { allMessages, setAiResponse, setMessages, setAllMessages } = useChat();
  const [currentStep, setCurrentStep] = useState(0);
  const [showSteps, setShowSteps] = useState(false);
  const chatContainerRef = useRef(null);
<<<<<<< Updated upstream
=======
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

  const handleRecipeSelection = async (selectedRecipe) => {
    if (!selectedRecipe) {
      console.error("❌ 선택한 레시피가 없습니다.");
      return;
    }

    setShowLoading(true);
  
    console.log(`✅ 선택한 요리: ${selectedRecipe}`);
  
    try {
      const response = await postQuery(selectedRecipe, optionCheck, "detail");
  
      console.log("🔍 상세 레시피 응답: ", response);
  
      if (response.recipe) {
        const newMessages = [
          { type: "text", content: `${response.recipe.title} 어떤가요?` },
          { type: "text", content: `📌 재료: ${response.recipe.ingredients.join(", ")}` },
          { type: "image", content: response.image_url },
          { type: "text", content: `${response.recipe.title}을 만들고 싶다면 "시작" 버튼을 눌러주세요` },
          { type: "recipe", recipe: response.recipe },
        ];
  
        for (let i = 0; i < newMessages.length; i++) {
          await new Promise((resolve) =>
            setTimeout(() => {
              setAiResponse((prev) => [...prev, newMessages[i]]);
              setAllMessages((prev) => [...prev, newMessages[i]]);
              resolve();
            }, i === 0 ? 300 : 1000)
          );
        }
      }
  
    } catch (error) {
      console.error("❌ 상세 레시피 요청 중 오류 발생:", error);
    }
    finally {
      setTimeout(() => setShowLoading(false), 400); // 🔹 로딩 종료 애니메이션 대기
    }
  };
  
>>>>>>> Stashed changes

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
    <div className="bg-white w-full h-full grow p-6 flex flex-col">
      <div
        ref={chatContainerRef}
        className="overflow-y-auto flex-grow max-h-[75vh] flex flex-col"
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
