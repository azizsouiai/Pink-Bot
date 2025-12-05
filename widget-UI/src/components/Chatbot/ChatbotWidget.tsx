import { useState, useRef, useEffect } from "react";
import type { FormEvent } from "react";
import { X, Send, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { cn } from "@/lib/utils";
import { useChatLogic } from "./useChatLogic";
import { ChatMessage, TypingIndicator } from "./ChatMessage";

// Importer les images
import ChatButtonIcon from "./assets/chatButton.png";

export const ChatbotWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [inputValue, setInputValue] = useState("");
  const { messages, loading, sendMessage, clearMessages } = useChatLogic();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-scroll vers le bas quand de nouveaux messages arrivent
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  // Focus sur l'input quand le widget s'ouvre
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 300);
    }
  }, [isOpen]);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !loading) {
      sendMessage(inputValue);
      setInputValue("");
    }
  };

  const handleToggle = () => {
    setIsOpen((prev) => !prev);
  };

  // État fermé - bouton flottant PNG qui dépasse du bord droit (effet "peeking")
  if (!isOpen) {
    return (
      <button
        onClick={handleToggle}
        className={cn(
          "fixed bottom-16 right-0 z-50",
          "w-20 h-28",
          "transition-all duration-300 hover:right-1",
          "focus:outline-none"
        )}
        aria-label="Ouvrir le chat"
      >
        <img
          src={ChatButtonIcon}
          alt="Ouvrir le Chatbot"
          className="w-full h-full object-contain"
          style={{ transform: "translateX(15%)" }}
        />
      </button>
    );
  }

  // État ouvert - fenêtre de chat style Messenger (Light Mode)
  return (
    <div
      className={cn(
        "fixed bottom-5 right-5 z-50",
        "w-[360px] h-[500px]",
        "flex flex-col",
        "bg-white rounded-2xl",
        "shadow-2xl shadow-black/20",
        "border border-gray-200",
        "overflow-hidden"
      )}
    >
      {/* En-tête */}
      <div className="flex items-center justify-between px-4 py-3 bg-linear-to-r from-[#1e3a5f] to-[#2c5282] border-b border-[#1e3a5f]">
        <div className="flex items-center gap-3">
          
          <div>
            <h3 className="font-semibold text-white text-sm">Assistant</h3>
            <p className="text-[11px] text-blue-200">toujours à votre assistance... 🙄</p>
          </div>
        </div>
        <div className="flex items-center gap-1">
          <Button
            variant="ghost"
            size="icon"
            onClick={clearMessages}
            className="h-8 w-8 text-white/80 hover:text-white hover:bg-white/20 rounded-full"
            title="Effacer le chat"
          >
            <Trash2 className="h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={handleToggle}
            className="h-8 w-8 text-white/80 hover:text-white hover:bg-white/20 rounded-full"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Zone des messages */}
      <ScrollArea className="flex-1 bg-gray-50">
        <div className="p-4 space-y-3 min-h-[340px]">
          {messages.map((msg) => (
            <ChatMessage key={msg.id} message={msg} />
          ))}
          {loading && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>
      </ScrollArea>

      {/* Zone de saisie */}
      <form
        onSubmit={handleSubmit}
        className="flex items-center gap-2 px-3 py-3 bg-white border-t border-gray-200"
      >
        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setInputValue(e.target.value)}
          placeholder="Écrivez votre message..."
          disabled={loading}
          className={cn(
            "flex-1 h-10 px-4 rounded-full",
            "bg-gray-100 border border-gray-200",
            "text-gray-900 text-sm placeholder:text-gray-400",
            "focus:outline-none focus:ring-2 focus:ring-[#1e3a5f]/50 focus:border-[#2c5282]",
            "disabled:opacity-50"
          )}
        />
        <Button
          type="submit"
          disabled={loading || !inputValue.trim()}
          size="icon"
          className={cn(
            "rounded-full h-10 w-10 shrink-0",
            "bg-[#1e3a5f] hover:bg-[#2c5282]",
            "text-white",
            "disabled:opacity-40"
          )}
        >
          <Send className="h-4 w-4" />
        </Button>
      </form>
    </div>
  );
};
