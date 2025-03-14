import React, { useMemo } from 'react';
import { useChat } from '../context/ChatContext';

const AllChatBubble = () => {
    const { allMessages } = useChat();
    const renderedMessages = useMemo(
      () =>
        allMessages.map((message, index) => (
          <div
            key={index}
            className={`chat ${message.type === "user" ? "chat-end" : "chat-start"}`}
          >
            <div
              className={`chat-bubble text-xl ${
                message.type === "user" ? "bg-sky-400" : "bg-yellow-400"
              }`}
            >
              {message.text}
            </div>
          </div>
        )),
      [allMessages]
    );
  
    return <div className="bg-white w-full p-4 flex flex-col gap-2">{renderedMessages}</div>;
  };

export default AllChatBubble;