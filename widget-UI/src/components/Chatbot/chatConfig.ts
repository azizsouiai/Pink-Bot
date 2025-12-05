// Configuration du Chat

// Point to Chatbruti API - use environment variable or default to localhost
export const CHAT_API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/chat";

// Types de personnages - "initial" pour le premier message, puis panther/inspector selon l'API
export type CharacterType = "initial" | "panther" | "inspector";

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  text: string;
  character?: CharacterType;
}

export interface ChatResponse {
  response: string;  // Chatbruti API returns 'response' not 'text'
  session_id: string;
  message_count: number;
}

// Générer un ID unique pour chaque message
export const generateMessageId = (): string => {
  return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
};

// Message d'accueil initial
export const INITIAL_MESSAGE: ChatMessage = {
  id: "initial_welcome",
  role: "assistant",
  text: "Bonjour ! Je suis votre assistant. Comment puis-je vous aider aujourd'hui ?",
  character: "initial",
};
