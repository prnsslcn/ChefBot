import { useEffect } from "react";
import { useChat } from "../context/ChatContext";
import { postQuery } from "../api/getQuery";
import { LoadingSpinner } from "./LoadingSpinner";

export const AiChatValidate = () => {
  const {
    callResponse,
    setAiResponse,
    setCallResponse,
    setAllMessages,
    allMessages,
    isAiResponding,
    setIsAiResponding,
    optionCheck,
    messages
  } = useChat();

  
  useEffect(() => {
    if (callResponse && !isAiResponding) {
      const fetchAiResponse = async () => {
        try {
          setIsAiResponding(true);
          // const response = await axios.get("http://localhost:5001/1");
          const response = await postQuery(messages[messages.length - 1])
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

          // 메시지를 하나씩 추가하는 함수
          const addMessagesSequentially = async () => {
            for (const message of newMessages) {
              await new Promise((resolve) => setTimeout(resolve, 1000)); // 1초 간격
              setAiResponse((prev) => [...prev, message]);
              setAllMessages((prev) => [...prev, message]);
            }

            // 마지막 메시지 추가 후 steps 저장
            setAllMessages((prev) => [
              ...prev,
              { recipe: { steps: response.recipe.steps } },
            ]);

            setIsAiResponding(false); // 메시지 추가 완료
          };

          addMessagesSequentially();
        } catch (error) {
          console.log(error);
          setIsAiResponding(false);
        }
      };

      fetchAiResponse();
      setCallResponse(false); // 통신 완료 후 callResponse 리셋
    }
  }, [callResponse, isAiResponding]);

  useEffect(() => {
    // allMessages가 업데이트되면 로그를 찍도록 추가
    console.log("Updated allMessages:", allMessages);
  }, [allMessages]); // allMessages가 변경될 때마다 실행됨

  return isAiResponding ? <LoadingSpinner /> : null;
};
