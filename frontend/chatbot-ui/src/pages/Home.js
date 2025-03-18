import { AiChatValidate } from "../components/AiChatValidate";
import AllChatBubble from "../components/AllChatBubble";
import { UserInput } from "../components/UserInput";

export default function Home() {
  return (
    <div className="bg-stone-200 p-10 min-h-screen flex flex-col">
      <AiChatValidate />
      <AllChatBubble />
      <UserInput />
    </div>
  );
}

/*
2025-03-17-14:40 pull develop
*/
