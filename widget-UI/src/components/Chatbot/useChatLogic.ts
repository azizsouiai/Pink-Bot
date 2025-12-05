import { useState } from "react";
import { CHAT_API_URL, generateMessageId, INITIAL_MESSAGE } from "./chatConfig";
import type { ChatMessage, CharacterType } from "./chatConfig";

export const useChatLogic = () => {
  // Commence avec le message d'accueil initial
  const [messages, setMessages] = useState<ChatMessage[]>([INITIAL_MESSAGE]);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);

  const sendMessage = async (userText: string) => {
    if (!userText.trim()) return;

    // Ajouter le message de l'utilisateur
    const userMessage: ChatMessage = {
      id: generateMessageId(),
      role: "user",
      text: userText,
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      console.log("Sending message to:", CHAT_API_URL);
      console.log("Request payload:", { message: userText, session_id: sessionId });
      
      const response = await fetch(CHAT_API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
          message: userText,
          session_id: sessionId  // Include session for conversation history
        }),
      });
      
      console.log("Response status:", response.status, response.statusText);

      if (!response.ok) {
        const errorText = await response.text();
        console.error("API Error:", response.status, errorText);
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Store session ID for future messages
      if (data.session_id) {
        setSessionId(data.session_id);
      }

      // Parse the response - Chatbruti returns JSON string with character info
      let responseText = data.response;
      let character: CharacterType = "panther"; // Default

      try {
        // Try to parse JSON response (from system prompt)
        const parsedResponse = JSON.parse(data.response);
        if (parsedResponse.response) {
          responseText = parsedResponse.response;
        }
        if (parsedResponse.character) {
          // Map character names to our types
          const charName = parsedResponse.character.toLowerCase();
          if (charName.includes("inspector") || charName.includes("dreyfus")) {
            character = "inspector";
          } else if (charName.includes("panther") || charName.includes("pink")) {
            character = "panther";
          }
        }
      } catch (e) {
        // If not JSON, use response as-is
        responseText = data.response;
      }

      const assistantMessage: ChatMessage = {
        id: generateMessageId(),
        role: "assistant",
        text: responseText,
        character: character,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Erreur lors de l'envoi du message:", error);
      
      // More detailed error message
      let errorText = "Oups ! Une erreur s'est produite. Veuillez réessayer.";
      
      if (error instanceof TypeError && error.message.includes("fetch")) {
        errorText = "Impossible de se connecter au serveur. Vérifiez que l'API est démarrée sur http://localhost:8000";
      } else if (error instanceof Error) {
        console.error("Error details:", error.message);
        errorText = `Erreur: ${error.message}`;
      }

      const errorMessage: ChatMessage = {
        id: generateMessageId(),
        role: "assistant",
        text: errorText,
        character: "panther",
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const clearMessages = () => {
    // Réinitialiser avec le message d'accueil et clear session
    setMessages([INITIAL_MESSAGE]);
    setSessionId(null); // Clear session to start fresh
  };

  return {
    messages,
    loading,
    sendMessage,
    clearMessages,
  };
};
