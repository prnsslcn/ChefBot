import React, { createContext, useContext, useState } from "react";

const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState([]);
  const [aiResponse, setAiResponse] = useState([]);
  const [callResponse, setCallResponse] = useState(false);
  const [allMessages, setAllMessages] = useState([
    "어떤 요리를 만들고 싶으세요?"
  ]);
  const [isAiResponding, setIsAiResponding] = useState(false);
  const [optionCheck, setOptionCheck] = useState("");

  return (
    <ChatContext.Provider
      value={{
        messages,
        setMessages,
        aiResponse,
        setAiResponse,
        callResponse,
        setCallResponse,
        allMessages,
        setAllMessages,
        isAiResponding,
        setIsAiResponding,
        optionCheck, setOptionCheck
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  return useContext(ChatContext);
};
