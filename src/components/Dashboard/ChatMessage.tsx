import React from 'react';
import { Bot, User } from 'lucide-react';
import { ChatMessage as ChatMessageType } from '../../types';

interface ChatMessageProps {
  message: ChatMessageType;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  console.log('ChatMessage component received:', message);
  
  const isAI = message.sender === 'ai';
  const time = new Date(message.timestamp).toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit' 
  });

  const formatMessage = (text: string) => {
    // Split text by newlines and wrap each line in <p> tags
    const lines = text.split('\n').filter(line => line.trim() !== '');
    
    return lines.map((line, index) => {
      // Apply markdown-like formatting
      const formattedLine = line
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/^(\d+\.\s)/g, '<strong>$1</strong>') // Bold numbered lists
        .replace(/^[-•]\s/g, '• '); // Convert dashes to bullets
      
      return `<p key="${index}" class="mb-2">${formattedLine}</p>`;
    }).join('');
  };

  return (
    <div className={`flex ${isAI ? 'justify-start' : 'justify-end'} mb-4`}>
      <div className={`flex max-w-[80%] ${isAI ? 'flex-row' : 'flex-row-reverse'}`}>
        <div className={`flex-shrink-0 ${isAI ? 'mr-3' : 'ml-3'}`}>
          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
            isAI 
              ? 'bg-gradient-to-r from-blue-600 to-indigo-700' 
              : 'bg-gradient-to-r from-gray-600 to-gray-700'
          }`}>
            {isAI ? (
              <Bot className="h-5 w-5 text-white" />
            ) : (
              <User className="h-5 w-5 text-white" />
            )}
          </div>
        </div>
        
        <div className={`flex flex-col ${isAI ? 'items-start' : 'items-end'}`}>
          <div className={`px-4 py-3 rounded-2xl ${
            isAI 
              ? 'bg-gray-100 text-gray-900 rounded-bl-sm border border-gray-200' 
              : 'bg-gradient-to-r from-blue-600 to-indigo-700 text-white rounded-br-sm'
          }`}>
            <div 
              className={`text-sm leading-relaxed ${isAI ? 'space-y-2' : ''}`}
              dangerouslySetInnerHTML={{ __html: formatMessage(message.text) }}
            />
          </div>
          <span className="text-xs text-gray-400 mt-1 px-2">
            {time}
          </span>
        </div>
      </div>
    </div>
  );
}
