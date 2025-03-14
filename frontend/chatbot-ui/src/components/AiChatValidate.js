import { useEffect, useMemo } from "react";
import { useChat } from "../context/ChatContext";
import { postQuery } from "../api/getQuery";

export const AiChatBubble = () => {
  const { aiResponse, callResponse, messages, setAiResponse, setCallResponse, setAllMessages, allMessages } = useChat();

  useEffect(() => {
    if (callResponse) {
      
      const latestMessage = messages[messages.length - 1];
      setAiResponse((prevResponse) => [...prevResponse, latestMessage]);
      setAllMessages((prevMessages) => [...prevMessages, {type: "ai", text: latestMessage}])
      setCallResponse(false);
      
    }
  }, [callResponse]);

  return null;
};

// export const UserChatBubble = () => {
//   const { messages } = useChat(); 
//   const renderedMessages = useMemo(() => (
//       messages.map((message, index) => (
//       <div key={index} className="chat chat-end my-4">
//           <div className="chat-bubble bg-sky-400 text-xl">
//           {message}
//           </div>
//       </div>
//       ))
//   ), [messages]); 

// return <div className="bg-white w-full p-4">{renderedMessages}</div>;
// };

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
