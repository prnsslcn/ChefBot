export const LoadingSpinner = () => {
  return (
    <div className="chat-message text-left mb-2 animate-fadein">
      <div className="inline-block px-4 py-2 rounded-xl bg-neutral-100 text-black w-[75px] shadow text-base h-[40px] flex items-center justify-center">
        <div className="flex space-x-2 items-center">
          <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounceUp"></span>
          <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounceUpDelayed1"></span>
          <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounceUpDelayed2"></span>
        </div>
      </div>
    </div>
  );
};
