import React, { useMemo, useState } from 'react';
import { useChat } from '../context/ChatContext';

const AllChatBubble = () => {
  const { allMessages } = useChat();
  const [showSteps, setShowSteps] = useState(false); 

  const renderedMessages = useMemo(() =>
    allMessages.map((message, index) => {
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
        <div key={index} className="chat chat-start">
          <div className="chat-bubble bg-yellow-400 text-xl">
            <div className="font-bold">{message.recipe.title}</div>
            <div>Ingredients:</div>
            <ul>
              {message.recipe.ingredients.map((ingredient, idx) => (
                <li key={idx}>{ingredient}</li>
              ))}
            </ul>
            <div className="flex justify-center items-center my-6">
                <button 
                className="btn bg-sky-400 w-1/3 text-2xl p-6"
                onClick={()=>setShowSteps(true)}
                >시작</button>
            </div>

            {showSteps && (
              <>
                <div>Steps:</div>
                <ol>
                  {message.recipe.steps.map((step, idx) => (
                    <li key={idx}>{step}</li>
                  ))}
                </ol>
                {message.image_url && (
                  <div>
                    <img src={message.image_url} alt="Recipe" className="w-32 h-32" />
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      );
    }),
    [allMessages, showSteps] 
  );

  return (
    <div className="bg-white w-full p-4 flex flex-col gap-2">
      {renderedMessages}
    </div>
  );
};

export default AllChatBubble;