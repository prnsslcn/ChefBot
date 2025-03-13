import { useEffect, useMemo } from "react";
import { useChat } from "../context/ChatContext";
import { postQuery } from "../api/getQuery";

export const AiChatBubble = () => {
  const { aiResponse, callResponse, messages, setAiResponse, setCallResponse } = useChat();

  useEffect(() => {
    if (callResponse) {
      const latestMessage = messages[messages.length - 1];
      setAiResponse((prevResponse) => [...prevResponse, latestMessage]);
      setCallResponse(false);
    }
  }, [callResponse, messages, setAiResponse, setCallResponse]);

  const renderedResponses = useMemo(
    () =>
      aiResponse.map((response, index) => (
        <div key={index} className="chat chat-start">
          <div className="chat-bubble bg-yellow-400 text-xl">{response}</div>
        </div>
      )),
    [aiResponse]
  );

  return (
    <div className="bg-white w-full flex-grow p-4">{renderedResponses}</div>
  );
};

// console.log(messages[messages.length - 1],aiResponse,callResponse)

// useEffect(() => {
//   if (callResponse) {
//     const latestMessage = messages[messages.length - 1];
//     const fetchAiResponse = async () => {
//       try {
//         const response = await postQuery(latestMessage);
//         setAiResponse([response.data]);
//         setCallResponse(false);
//       } catch (error) {
//         console.error('API 호출 실패:', error);
//         setCallResponse(false);
//       }
//     };
//     fetchAiResponse();
//   }
// }, [callResponse]);
