import { AiChatValidate } from "../components/AiChatValidate";
import AllChatBubble from "../components/AllChatBubble";
import { UserInput } from "../components/UserInput";

export default function Home() {
  return (
    <div className="w-full h-screen bg-white flex items-center justify-center">
      <div className="w-[95%] max-w-[800px] h-[95%] bg-white rounded-2xl shadow-lg flex flex-col justify-between border border-neutral-200 overflow-hidden">
        <div className="flex justify-center items-center p-4 border-b border-neutral-300">
          <img src="https://img.icons8.com/stickers/100/cook-male.png" alt="Chatbot Logo" className="h-12" />
        </div>
        <AiChatValidate />
        <AllChatBubble />
        <UserInput />
      </div>
    </div>
  );
}
