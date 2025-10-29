export const TypingIndicator = () => {
  return (
    <div className="w-full py-8 px-4 bg-chat-message-ai">
      <div className="max-w-3xl mx-auto flex gap-6">
        <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-muted flex items-center justify-center font-semibold text-sm">
          BT
        </div>
        <div className="flex-1 space-y-2">
          <p className="text-sm font-medium text-muted-foreground">BALLTALK</p>
          <div className="flex gap-1 items-center h-6">
            <div className="w-2 h-2 rounded-full bg-primary animate-bounce [animation-delay:-0.3s]"></div>
            <div className="w-2 h-2 rounded-full bg-primary animate-bounce [animation-delay:-0.15s]"></div>
            <div className="w-2 h-2 rounded-full bg-primary animate-bounce"></div>
          </div>
        </div>
      </div>
    </div>
  );
};
