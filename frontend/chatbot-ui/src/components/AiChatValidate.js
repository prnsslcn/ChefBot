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
          const response = await postQuery(messages[messages.length - 1], optionCheck)
          console.log("대답 : ",response)
          // ai 레시피 제안
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
              content: `${response.recipe.title}을 만들고 싶다면 "시작" 버튼을 눌러주세요`,
            },
          ];

          const addMessagesSequentially = async () => {
            for (let i = 0; i < newMessages.length; i++) {
              if(i === 0){
                await new Promise((resolve) => setTimeout(resolve, 300));
              }
              else if (i !== 0) {
                await new Promise((resolve) => setTimeout(resolve, 1000));
              }
              setAiResponse((prev) => [...prev, newMessages[i]]);
              setAllMessages((prev) => [...prev, newMessages[i]]);
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
    // allMessages가 업데이트되면 로그를 찍도록 추가
    console.log("Updated allMessages:", allMessages);
  }, [allMessages]); // allMessages가 변경될 때마다 실행됨

  return null;
};
