import { cn } from "@/lib/utils";
import ResponseBox from "./ResponseBox"; // ✅ import your new Markdown component

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
}

export const ChatMessage = ({ role, content }: ChatMessageProps) => {
  const isUser = role === "user";

  return (
    <div
      className={cn(
        "w-full py-8 px-4 transition-colors chat-message-enter",
        isUser
          ? "bg-chat-message-user"
          : "bg-chat-message-ai hover:bg-chat-message-hover"
      )}
    >
      <div className="max-w-3xl mx-auto flex gap-6">
        <div
          className={cn(
            "flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center font-semibold text-sm",
            isUser
              ? "bg-primary text-primary-foreground"
              : "bg-muted text-foreground"
          )}
        >
          {isUser ? "U" : "BT"}
        </div>

        <div className="flex-1 space-y-2">
          <p className="text-sm font-medium text-muted-foreground">
            {isUser ? "You" : "BALLTALK"}
          </p>

          {/* ✅ If AI message → render Markdown; else render plain text */}
          <div className="text-foreground leading-relaxed whitespace-pre-wrap">
            {isUser ? (
              content
            ) : (
              <ResponseBox text={content} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
