import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { UserInput } from "../components/UserInput";
import { postQuery } from "../api/getQuery";
import { AiChatBubble } from "../components/AiChatBubble";

export default function Home() {

    const [messages, setMessages] = useState([]);
    const [aiResponse, setAiResponse] = useState(['어떤 요리를 만들고 싶으세요?']);
    const chatEndRef = useRef(null); 

    const handleSendMessage = useCallback( async (input) => {
        setMessages((prevMessages) => [...prevMessages, input ]);
        try {
            const response = await postQuery(input);
            setAiResponse(response);
        } catch (error) {
            console.error('API 요청 오류:', error);

        }
    }, []);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const renderedMessages = useMemo(() => (
        messages.map((message, index) => (
            <div key={index} className="chat chat-end my-4">
                <div className="chat-bubble bg-sky-400 text-xl">
                    {message}
                </div>
            </div>
        ))
    ), [messages]);

    return (
      <div className="bg-gray-300 p-10 min-h-screen flex flex-col">
        <div className="bg-white w-full flex-grow p-4">
          <div className="chat chat-start">
            <div className="chat-bubble bg-yellow-400 text-xl">
                <AiChatBubble aiResponse={aiResponse} />
            </div>
          </div>
        </div>
        
        <div className="bg-white w-full p-4">
                {renderedMessages}
                <div ref={chatEndRef} />
        </div>

        
        <UserInput onSendMessage={handleSendMessage} />
      </div>
    );
  }
  
// export default function Home() {
//     return (
//       <div className="bg-gray-300 p-10 min-h-screen flex flex-col">
//         <div className="bg-white w-full flex-grow p-4">
//           <div className="chat chat-start">
//             <div className="chat-bubble bg-yellow-400 text-xl">
//               어떤 요리를 만들고 싶으신가요?
//             </div>
//           </div>
//           <div className="chat chat-end my-4">
//             <div className="chat-bubble bg-orange-400 text-xl">
//               치즈, 감자를 이용한 요리를 알려줘
//             </div>
//           </div>
//           <div className="chat chat-start">
//             <div className="chat-bubble bg-yellow-400 text-xl">
//               치즈그라탕 어떤가요?
//             </div>
//           </div>
//           <div className="chat chat-start">
//             <div className="chat-bubble bg-yellow-400 text-xl">
//               📌 재료
//               <br />
//               감자: 3개, 200g 치즈, 생크림 1컵, 소금, 후추
//             </div>
//           </div>
//           <div className="chat chat-start">
//             <div className="chat-bubble bg-yellow-400 text-xl">
//               <img
//                 alt="치즈 그라탕"
//                 className="w-full h-64 rounded-lg"
//               />
//             </div>
//           </div>
//           <div className="chat chat-start">
//             <div className="chat-bubble bg-yellow-400 text-xl text-sky-900">
//               치즈그라탕을 만들고 싶다면 "시작"버튼을 눌러주세요
//             </div>
//           </div>
//           <div className="flex justify-center items-center my-6">
//             <button className="btn bg-sky-400 w-1/3 text-2xl p-6">시작</button>
//           </div>
//           {/* <div>
//             <div className="chat chat-start">
//               <div className="chat-bubble bg-yellow-400 text-xl">
//                 Step 1: 감자를 얇게 잘라주세요
//                 <br />다 되었다면 "다음"버튼을 눌러주세요
//               </div>
//             </div>
//             <div className="flex justify-center items-center my-6">
//               <button className="btn bg-emerald-400 text-emerald-900 w-1/3 text-2xl p-6">
//                 다음
//               </button>
//             </div>
//             <div className="chat chat-start">
//               <div className="chat-bubble bg-yellow-400 text-xl">
//                 🎉 완료! 200°C 오븐에서 30분간 구우면 맛있는 치즈 감자 그라탕이
//                 완성됩니다! 😋
//               </div>
//             </div>
//             <div className="chat chat-start">
//               <div className="chat-bubble bg-yellow-400 text-xl">
//                 다른 레시피를 시도해보고 싶다면 "다시 시작" 버튼을 눌러주세요!
//               </div>
//             </div>
//             <div className="flex justify-center items-center my-6">
//               <button className="btn bg-red-400 text-red-900 w-1/3 text-2xl p-6">
//                 다시 시작
//               </button>
//             </div>
//           </div> */}
//           <div>
//             <ul className="steps steps-vertical">
//               <li className="step step-info">Fly to moon</li>
//               <li className="step step-info">Shrink the moon</li>
//               <li className="step step-info">Grab the moon</li>
//               <li className="step step-error" data-content="?">
//                 Sit on toilet
//               </li>
//             </ul>
//             <ul className="steps">
//               <li className="step step-primary">Register</li>
//               <li className="step step-primary">Choose plan</li>
//               <li className="step">Purchase</li>
//               <li className="step">Receive Product</li>
//             </ul>
//           </div>
//         </div>
  
//         <div className="bg-white p-4">
//           <input
//             type="text"
//             placeholder="만들고 싶은 요리를 입력해주세요"
//             className="input input-xl w-full focus:outline-none"
//           />
//           <button className="btn btn-outline">sned</button>
//         </div>
//       </div>
//     );
//   }