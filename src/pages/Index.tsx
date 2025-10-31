import { useState, useEffect, useRef } from "react";
import { ChatMessage } from "@/components/ChatMessage";
import { ChatInput } from "@/components/ChatInput";
import { TypingIndicator } from "@/components/TypingIndicator";
import { BasketballLogo } from "@/components/BasketballLogo";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  chartImage?: string | null;
  chartTitle?: string | null;
}

const Index = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsTyping(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: content }),
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      const data = await response.json();

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.reply || "No reply received.",
        chartImage: data.chart_image || null,
        chartTitle: data.chart_title || null,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error("Error connecting to backend:", error);
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: "⚠️ Server error. Please try again.",
        },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-chat-bg">
      {/* Header */}
      <header className="border-b border-border bg-background/95 backdrop-blur sticky top-0 z-10">
        <div className="max-w-3xl mx-auto px-4 py-4 flex items-center justify-center">
          <BasketballLogo />
        </div>
      </header>

      {/* Messages */}
      <main className="flex-1 overflow-y-auto">
        <div className="min-h-full space-y-2">
          {messages.map((message) => (
            <div key={message.id}>
              <ChatMessage role={message.role} content={message.content} />
              
              {/* 🧩 Chart rendering */}
              {message.role === "assistant" && message.chartImage && (
                <div className="flex justify-center mt-4 mb-8">
                  <div className="bg-secondary p-4 rounded-2xl shadow-md max-w-2xl">
                    {message.chartTitle && (
                      <p className="text-center text-sm font-medium text-muted-foreground mb-2">
                        {message.chartTitle}
                      </p>
                    )}
                    <img
                      src={
                        message.chartImage.startsWith("data:image")
                          ? message.chartImage
                          : `data:image/png;base64,${message.chartImage}`
                      }
                      alt={message.chartTitle || "Visualization"}
                      className="rounded-xl border border-border max-h-[400px] mx-auto"
                    />
                  </div>
                </div>
              )}
            </div>
          ))}
          {isTyping && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input */}
      <ChatInput onSend={handleSend} disabled={isTyping} />
    </div>
  );
};

export default Index;
