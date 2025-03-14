import { useEffect } from "react";
import { useChat } from "../context/ChatContext";
// import { postQuery } from "../api/getQuery";
import axios from "axios";

export const AiChatValidate = () => {
  const { callResponse, setAiResponse, setCallResponse, setAllMessages} = useChat();


  useEffect(() => {
    if (callResponse) {
      const fetchAiResponse = async () => {
        try {
          const response = await axios.get('http://localhost:5000/0');
          setAiResponse((prevResponse) => [...prevResponse, response.data]);
          setAllMessages((prevMessages) => [...prevMessages, response.data])
        } catch (error) {
          console.log(error);
        }
      }
      fetchAiResponse();
      setCallResponse(false);
    }
  }, [callResponse]);

  return null;
};