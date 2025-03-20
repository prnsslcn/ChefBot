export const LoadingSpinner = () => {
  return (
    <div className="chat-message text-left mb-2 animate-fadein">
      <div className="inline-block px-4 py-2 rounded-xl bg-neutral-100 text-black max-w-[70%] shadow text-base">
        <div className="loading loading-dots loading-lg">...</div>
      </div>
    </div>
  );
};
