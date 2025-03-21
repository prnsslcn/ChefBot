import { useEffect, useRef, useState, useMemo } from "react";
import { useChat } from "../context/ChatContext";
import { postQuery } from "../api/getQuery";
import { LoadingSpinner } from "./LoadingSpinner";

const AllChatBubble = () => {
  const {
    allMessages,
    setAiResponse,
    setMessages,
    setAllMessages,
    callResponse,
    setStepMode,
    optionCheck,
  } = useChat();

  const [currentStep, setCurrentStep] = useState(0);
  const [showSteps, setShowSteps] = useState(false);
  const [showLoading, setShowLoading] = useState(false);
  const chatContainerRef = useRef(null);

  useEffect(() => {
    if (callResponse) {
      setShowLoading(true);
    } else {
      const timeout = setTimeout(() => setShowLoading(false), 400);
      return () => clearTimeout(timeout);
    }
  }, [callResponse]);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTo({
        top: chatContainerRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [allMessages, currentStep]);

  const handleRecipeSelection = async (selectedRecipe) => {
    if (!selectedRecipe) return;

    setShowLoading(true);

    try {
      const response = await postQuery(selectedRecipe, optionCheck, "detail");

      if (response.recipe) {
        const initialMessages = [
          { type: "text", content: `${response.recipe.title} 어떤가요?` },
          { type: "text", content: `📌 재료: ${response.recipe.ingredients.join(", ")}` },
        ];

        for (let msg of initialMessages) {
          await new Promise((resolve) => {
            setTimeout(() => {
              setAiResponse((prev) => [...prev, msg]);
              setAllMessages((prev) => [...prev, msg]);
              resolve();
            }, 800);
          });
        }

        const imageMessage = { type: "image", content: response.image_url };
        const imageLoadPromise = new Promise((resolve) => {
          const img = new Image();
          img.src = response.image_url;
          img.onload = () => resolve();
        });

        setAiResponse((prev) => [...prev, imageMessage]);
        setAllMessages((prev) => [...prev, imageMessage]);

        await imageLoadPromise;

        const finalText = {
          type: "text",
          content: `${response.recipe.title}을 만들고 싶다면 \"시작\" 버튼을 눌러주세요`,
        };

        await new Promise((resolve) => {
          setTimeout(() => {
            setAiResponse((prev) => [...prev, finalText]);
            setAllMessages((prev) => [...prev, finalText]);
            resolve();
          }, 700);
        });

        const recipeData = { type: "recipe", recipe: response.recipe };
        setAiResponse((prev) => [...prev, recipeData]);
        setAllMessages((prev) => [...prev, recipeData]);
      }
    } catch (error) {
      console.error("레시피 요청 오류", error);
    } finally {
      setTimeout(() => setShowLoading(false), 400);
    }
  };

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

  const renderedMessages = useMemo(() =>
    allMessages.map((message, index) => {
      if (typeof message === "string") {
        const isUser = message !== "어떤 요리를 만들고 싶으세요?";
        return (
          <div key={index} className={`chat-message ${isUser ? "text-right" : "text-left"} mb-2 animate-fadein`}>
            <div className={`inline-block px-4 py-2 rounded-xl max-w-[70%] text-base ${isUser ? "bg-sky-500 text-white ml-auto" : "bg-neutral-100 text-black mr-auto"} shadow`}>
              {message}
            </div>
          </div>
        );
      }
      if (typeof message === "object" && message.type === "buttons") {
        return (
          <div key={index} className="chat-message text-left mb-2 animate-fadein">
            <div className="flex space-x-2">
              {message.options.map((option, idx) => (
                <button
                  key={idx}
                  className="bg-blue-500 text-white px-4 py-2 rounded-lg shadow"
                  onClick={() => handleRecipeSelection(option)}
                >
                  {option}
                </button>
              ))}
            </div>
          </div>
        );
      }
      if (typeof message === "object" && message?.content) {
        return (
          <div key={index} className="chat-message text-left mb-2 animate-fadein">
            {message.type === "text" ? (
              <div className="inline-block px-4 py-2 rounded-xl bg-neutral-100 text-black max-w-[70%] shadow text-base">
                {message.content}
              </div>
            ) : (
              <img
                src={message.content}
                alt="요리 이미지"
                className="w-full max-w-80 h-80 rounded-lg object-cover animate-fadein"
              />
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
            <button
              className="bg-sky-500 hover:bg-sky-700 text-white text-lg px-6 py-3 rounded-lg shadow"
              onClick={() => setShowSteps(true)}
            >
              시작
            </button>
          ) : (
            <div className="w-full mt-4">
              <ul className="space-y-2 text-left text-base">
                {allMessages.find((msg) => msg?.recipe?.steps)?.recipe?.steps?.slice(0, currentStep + 1).map((step, idx) => (
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
