export const AiChatBubble = ({ aiResponse }) => {
  return (
    <div>
      {aiResponse.map((response, index) => (
        <div key={index}>
          {response} 
        </div>
      ))}
    </div>
  );
};