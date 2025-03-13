import { AiChatBubble } from "../components/AiChatBubble";
import { UserChatBubble } from "../components/UserChatBubble";
import { UserInput } from "../components/UserInput";

export default function Home() {

    return (
        <div className="bg-gray-300 p-10 min-h-screen flex flex-col">
            <AiChatBubble/>
            <UserChatBubble/>
            <UserInput/>
        </div>
    );
}