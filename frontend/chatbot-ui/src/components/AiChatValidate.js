import { useEffect } from "react";
import { useChat } from "../context/ChatContext";
import { postQuery } from "../api/getQuery";

export const AiChatValidate = () => {
  const {
    callResponse,
    setAiResponse,
    setCallResponse,
    setAllMessages,
    allMessages,
    isAiResponding,
    setIsAiResponding,
    messages,
    setMessages,
    optionCheck,
    setShowSteps,
    setStepMode,
  } = useChat();

  useEffect(() => {
    if (callResponse && !isAiResponding) {
      const fetchAiResponse = async () => {
        try {
          setIsAiResponding(true);

          if (!messages || messages.length === 0) return;

          const lastUserMessage = messages[messages.length - 1];
          if (!lastUserMessage) return;

          console.log("🔍 Fetching AI response for:", lastUserMessage);
          const response = await postQuery(lastUserMessage, optionCheck, "select");

          console.log("대답 : ", response);

          // 1️⃣ 추천 요리가 여러 개일 경우, 버튼을 제공
          const newMessages = [
            {
              type: "text",
              content: `입력하신 메뉴(재료) 기반 음식입니다! 선택해주세요👇 `,
            },
            {
              type: "buttons", // 새로운 타입 추가 (추천 요리 선택 버튼)
              options: response.recipes, // 버튼에 표시될 요리 목록
            },
          ];

          const addMessagesSequentially = async () => {
            for (let i = 0; i < newMessages.length; i++) {
              const currentMsg = newMessages[i];

              await new Promise((resolve) =>
                setTimeout(() => {
                  setAiResponse((prev) => [...prev, currentMsg]);
                  setAllMessages((prev) => [...prev, currentMsg]);
                  resolve();
                }, i === 0 ? 300 : 1000)
              );
            }

            setIsAiResponding(false);
          };

          setCallResponse(false);
          addMessagesSequentially();
        } catch (error) {
          alert("에러");
          setCallResponse(false);
          setIsAiResponding(false);
          setAiResponse([]);
          setMessages([]);
          setAllMessages(["어떤 요리를 만들고 싶으세요?"]);
          setShowSteps(false);
          setStepMode(false);
        }
      };
      fetchAiResponse();
    }
  }, [callResponse, isAiResponding]);

  useEffect(() => {
    console.log("Updated allMessages:", allMessages);
  }, [allMessages]);

  return null;
};
