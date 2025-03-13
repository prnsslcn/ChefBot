import { useMemo } from "react";
import { useChat } from "../context/ChatContext"; 

export const UserChatBubble = () => {
    const { messages } = useChat(); 
    const renderedMessages = useMemo(() => (
        messages.map((message, index) => (
        <div key={index} className="chat chat-end my-4">
            <div className="chat-bubble bg-sky-400 text-xl">
            {message}
            </div>
        </div>
        ))
    ), [messages]); 

  return <div className="bg-white w-full p-4">{renderedMessages}</div>;
};