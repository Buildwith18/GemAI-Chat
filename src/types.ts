export interface User {
  id: string;
  name: string;
  email: string;
  joinDate: string;
  skillsLearned: string[];
  totalChats: number;
}

export interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: string;
  skillCategory?: string;
}

export interface ChatSession {
  id: string;
  userId: string;
  messages: ChatMessage[];
  startTime: string;
  title: string;
}
