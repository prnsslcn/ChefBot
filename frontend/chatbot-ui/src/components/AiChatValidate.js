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
    setStepMode
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
          const response = await postQuery(lastUserMessage, optionCheck);

          console.log("대답 : ", response);

          const newMessages = [
            {
              type: "text",
              content: `${response.recipe.title} 어떤가요?`,
            },
            {
              type: "text",
              content: `📌 재료 : ${response.recipe.ingredients}`,
            },
            { type: "image", content: response.image_url },
            {
              type: "text",
              content: `${response.recipe.title}을 만들고 싶다면 \"시작\" 버튼을 눌러주세요`,
            },
          ];

          const addMessagesSequentially = async () => {
            for (let i = 0; i < newMessages.length; i++) {
              const currentMsg = newMessages[i];

              if (currentMsg.type === "image") {
                const img = new Image();
                img.src = currentMsg.content;

                await new Promise((resolve) => {
                  img.onload = () => {
                    setAiResponse((prev) => [...prev, currentMsg]);
                    setAllMessages((prev) => [...prev, currentMsg]);
                    resolve();
                  };
                });
              } else {
                await new Promise((resolve) =>
                  setTimeout(() => {
                    setAiResponse((prev) => [...prev, currentMsg]);
                    setAllMessages((prev) => [...prev, currentMsg]);
                    resolve();
                  }, i === 0 ? 300 : 1000)
                );
              }
            }

            setAllMessages((prev) => [
              ...prev,
              { recipe: { steps: response.recipe.steps } },
            ]);

            setIsAiResponding(false);
          };

          setCallResponse(false);
          addMessagesSequentially();
        } catch (error) {
          alert('에러');
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
