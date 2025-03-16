import React, { useMemo, useState } from 'react';
import { useChat } from '../context/ChatContext';

const AllChatBubble = () => {
  const { allMessages,setAllMessages,setAiResponse, setMessages } = useChat();
  const [showSteps, setShowSteps] = useState(false); 
  const [showImage, setShowImage] = useState(false); 

  const handleReTry = () => {
    setShowSteps(false);
    setShowImage(false);
    setAiResponse([]);
    setMessages([]);
    setAllMessages(['어떤 요리를 만들고 싶으세요?']);
  }


  console.log(allMessages)

  const renderedMessages = useMemo(() =>
    allMessages.map((message, index) => {
        console.log(allMessages)
      if (typeof message === "string") {
        if (message === "어떤 요리를 만들고 싶으세요?") {
          return (
            <div key={index} className="chat chat-start">
              <div className="chat-bubble text-xl bg-yellow-400">
                {message}
              </div>
            </div>
          );
        }

        return (
          <div key={index} className="chat chat-end">
            <div className="chat-bubble text-xl bg-sky-400">
              {message}
            </div>
          </div>
        );
      }

      return (
        <>
          <div key={index} className="chat chat-start">
            <div className="chat-bubble bg-yellow-400 text-xl">
              <div className="font-bold">{message.recipe.title}</div>
              <div>Ingredients:</div>
              <ul>
                {message.recipe.ingredients.map((ingredient, idx) => (
                  <li key={idx}>{ingredient}</li>
                ))}
              </ul>
            </div>
          </div>
          <div className="flex justify-center items-center my-6">
            <button
              className="btn bg-sky-400 w-1/3 text-2xl p-6"
              onClick={() => setShowSteps(true)}
            >
              시작
            </button>
          </div>

          {showSteps && (
            <>
              <div className="chat chat-start">
                <div className="chat-bubble bg-yellow-400 text-xl">
                  <div>Steps:</div>
                  <ol>
                    {message.recipe.steps.map((step, idx) => (
                      <li key={idx}>{step}</li>
                    ))}
                  </ol>
                </div>
              </div>

              <div className="flex justify-center items-center my-6">
                <button
                  className="btn bg-emerald-400 text-emerald-900 w-1/3 text-2xl p-6"
                  onClick={() => setShowImage(true)}
                >
                  다음
                </button>
              </div>
            </>
          )}

          {message.image_url && showImage && (
            <>
              <div className="chat chat-start">
                <div className="chat-bubble bg-yellow-400 text-xl">
                  <img
                    src={message.image_url}
                    alt="Recipe"
                    className="w-32 h-32"
                  />
                </div>
              </div>

              <div className="flex justify-center items-center my-6">
                <button 
                className="btn bg-red-400 text-red-900 w-1/3 text-2xl p-6"
                onClick={() => handleReTry()}
                >
                  다시 시작
                </button>
              </div>
            </>
          )}
        </>
      );
    }),
    [allMessages, showSteps,showImage] 
  );

  return (
    <div className="bg-white w-full p-4 flex flex-col gap-2">
      {renderedMessages}
    </div>
  );
};

export default AllChatBubble;