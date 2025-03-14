import { AiChatBubble } from "../components/AiChatValidate";
import AllChatBubble from "../components/AllChatBubble";
import { UserInput } from "../components/UserInput";

export default function Home() {

    return (
        <div className="bg-gray-300 p-10 min-h-screen flex flex-col">
            <AiChatBubble/>
            <AllChatBubble/>
            <UserInput/>
        </div>
    );
}