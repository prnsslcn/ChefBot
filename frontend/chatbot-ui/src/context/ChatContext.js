import React, { createContext, useContext, useState } from 'react';

const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
    const [messages, setMessages] = useState([]);
    const [aiResponse, setAiResponse] = useState(['어떤 요리를 만들고 싶으세요?']);
    const [callResponse, setCallResponse] = useState(false);

    return (
        <ChatContext.Provider value={{ messages, setMessages, aiResponse, setAiResponse, callResponse, setCallResponse }}>
            {children}
        </ChatContext.Provider>
    );
};

export const useChat = () => {
    return useContext(ChatContext);
};