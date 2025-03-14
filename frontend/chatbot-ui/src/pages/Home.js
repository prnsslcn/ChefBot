import { AiChatValidate } from "../components/AiChatValidate";
import AllChatBubble from "../components/AllChatBubble";
import { UserInput } from "../components/UserInput";

export default function Home() {

    return (
        <div className="bg-gray-300 p-10 min-h-screen flex flex-col">
            <AiChatValidate/>
            <AllChatBubble/>
            <UserInput/>
        </div>
    );
}

/*
시작 버튼
        <div className="flex justify-center items-center my-6">
            <button className="btn bg-sky-400 w-1/3 text-2xl p-6">시작</button>
        </div>

다음 버튼
          <div className="flex justify-center items-center my-6">
            <button className="btn bg-emerald-400 text-emerald-900 w-1/3 text-2xl p-6">
              다음
            </button>
          </div>
          <div className="chat chat-start">

다시 시작
          <div className="flex justify-center items-center my-6">
            <button className="btn bg-red-400 text-red-900 w-1/3 text-2xl p-6">
              다시 시작
            </button>
          </div>
*/

