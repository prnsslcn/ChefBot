import { ChatProvider } from "./context/ChatContext";
import Home from "./pages/Home";

function App() {

  return (
    <ChatProvider>
      <Home/>
    </ChatProvider>
  );
}

export default App;