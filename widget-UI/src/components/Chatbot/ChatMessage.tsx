import type { FC } from "react";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";
import type { ChatMessage as ChatMessageType, CharacterType } from "./chatConfig";

// Importer les icônes des personnages
import InitialIcon from "./assets/initial.png";
import PantherIcon from "./assets/pink.png";
import InspectorIcon from "./assets/inspector.png"; // Remplacez par l'icône de l'inspecteur

// Mapping des icônes selon le type de personnage
const CHARACTER_ICONS: Record<CharacterType, string> = {
  initial: InitialIcon,      // Icône initiale pour le message d'accueil
  panther: PantherIcon,      // Icône de la panthère
  inspector: InspectorIcon,  // Icône de l'inspecteur
};

interface ChatMessageProps {
  message: ChatMessageType;
}

export const ChatMessage: FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === "user";

  // Obtenir l'icône appropriée selon l'attribut "character" du JSON
  const getCharacterIcon = () => {
    if (message.character && CHARACTER_ICONS[message.character]) {
      return CHARACTER_ICONS[message.character];
    }
    return InitialIcon; // Par défaut, utiliser l'icône initiale
  };

  if (isUser) {
    // Message utilisateur - style Messenger : bulle à droite (Navy Blue)
    return (
      <div className="flex justify-end pl-12">
        <div
          className={cn(
            "px-3.5 py-2 rounded-2xl rounded-br-md",
            "bg-[#1e3a5f] text-white",
            "shadow-sm"
          )}
        >
          <p className="text-[14px] leading-relaxed">{message.text}</p>
        </div>
      </div>
    );
  }

  // Message du bot - style Messenger Light Mode : petit avatar + bulle
  return (
    <div className="flex justify-start items-end gap-2 pr-12">
      <Avatar className="h-7 w-7 shrink-0 ring-1 ring-gray-200">
        <AvatarImage src={getCharacterIcon()} alt={message.character || "bot"} />
        <AvatarFallback className="text-xs bg-blue-100">🐆</AvatarFallback>
      </Avatar>
      <div
        className={cn(
          "px-3.5 py-2 rounded-2xl rounded-bl-md",
          "bg-gray-200 text-gray-900",
          "shadow-sm"
        )}
      >
        <p className="text-[14px] leading-relaxed">{message.text}</p>
      </div>
    </div>
  );
};

export const TypingIndicator: FC = () => {
  return (
    <div className="flex justify-start items-end gap-2 pr-12">
      <Avatar className="h-7 w-7 shrink-0 ring-1 ring-gray-200">
        <AvatarImage src={CHARACTER_ICONS.initial} alt="en train d'écrire" />
        <AvatarFallback className="text-xs bg-blue-100">🐆</AvatarFallback>
      </Avatar>
      <div className="bg-gray-200 px-4 py-3 rounded-2xl rounded-bl-md shadow-sm">
        <div className="flex gap-1">
          <span 
            className="w-2 h-2 bg-gray-400 rounded-full"
            style={{ animation: "bounce 1.4s ease-in-out infinite", animationDelay: "0ms" }}
          />
          <span 
            className="w-2 h-2 bg-gray-400 rounded-full"
            style={{ animation: "bounce 1.4s ease-in-out infinite", animationDelay: "200ms" }}
          />
          <span 
            className="w-2 h-2 bg-gray-400 rounded-full"
            style={{ animation: "bounce 1.4s ease-in-out infinite", animationDelay: "400ms" }}
          />
        </div>
      </div>
    </div>
  );
};
