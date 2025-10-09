import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Sparkles, Copy, Trash2, Plus, MessageSquare } from 'lucide-react';
import { ChatMessage } from '../../types';
import { useAuth } from '../../contexts/AuthContext';
import ChatMessageComponent from './ChatMessage';
import TypingIndicator from './TypingIndicator';

interface ChatSession {
  session_id: string;
  created_at: string;
  message_count: number;
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId, setSessionId] = useState<string>('default');
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [showSessions, setShowSessions] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { user, updateUser } = useAuth();

  const scrollToBottom = () => {
    setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  useEffect(() => {
    // Load chat history from database
    loadChatHistory();
    loadSessions();

    // Listen for quick prompts
    const handleQuickPrompt = (event: CustomEvent) => {
      setInputText(event.detail);
    };

    window.addEventListener('quickPrompt', handleQuickPrompt as EventListener);
    return () => window.removeEventListener('quickPrompt', handleQuickPrompt as EventListener);
  }, [user, sessionId]);

  useEffect(() => {
    // Messages are now saved to database automatically by the backend
    // No need to save to localStorage
  }, [messages, user]);

  const generateNewSessionId = () => {
    return `session_${user?.id || 'anonymous'}_${Date.now()}`;
  };

  const loadChatHistory = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/history/?user_id=${user?.id || 'anonymous'}&session_id=${sessionId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        if (data.messages && data.messages.length > 0) {
          console.log('Loaded chat history from database:', data.messages);
          setMessages(data.messages);
        } else {
          // Add welcome message if no history
          const welcomeMessage: ChatMessage = {
            id: '1',
            text: `Hello ${user?.name}! I'm your AI tutor, ready to help you learn and grow. What would you like to explore today?`,
            sender: 'ai',
            timestamp: new Date().toISOString(),
          };
          setMessages([welcomeMessage]);
        }
      } else {
        console.error('Failed to load chat history:', response.status);
        // Add welcome message as fallback
        const welcomeMessage: ChatMessage = {
          id: '1',
          text: `Hello ${user?.name}! I'm your AI tutor, ready to help you learn and grow. What would you like to explore today?`,
          sender: 'ai',
          timestamp: new Date().toISOString(),
        };
        setMessages([welcomeMessage]);
      }
    } catch (error) {
      console.error('Error loading chat history:', error);
      // Add welcome message as fallback
      const welcomeMessage: ChatMessage = {
        id: '1',
        text: `Hello ${user?.name}! I'm your AI tutor, ready to help you learn and grow. What would you like to explore today?`,
        sender: 'ai',
        timestamp: new Date().toISOString(),
      };
      setMessages([welcomeMessage]);
    }
  };

  const loadSessions = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/sessions/?user_id=${user?.id || 'anonymous'}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setSessions(data.sessions || []);
      }
    } catch (error) {
      console.error('Error loading sessions:', error);
    }
  };

  const startNewChat = () => {
    const newSessionId = generateNewSessionId();
    setSessionId(newSessionId);
    const welcomeMessage: ChatMessage = {
      id: '1',
      text: `Hello ${user?.name}! I'm your AI tutor, ready to help you learn and grow. What would you like to explore today?`,
      sender: 'ai',
      timestamp: new Date().toISOString(),
    };
    setMessages([welcomeMessage]);
    setShowSessions(false);
  };

  const switchToSession = (sessionId: string) => {
    setSessionId(sessionId);
    setShowSessions(false);
  };

  const callBackendAPI = async (userMessage: string): Promise<string> => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          prompt: userMessage,
          user_id: user?.id || 'anonymous',
          session_id: sessionId
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }

      return data.reply || 'I apologize, but I couldn\'t generate a response at the moment. Please try again.';
    } catch (error) {
      console.error('Error calling backend API:', error);
      return 'I apologize, but I\'m having trouble connecting to my AI service right now. Please check your internet connection and try again.';
    }
  };

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    console.log('=== SENDING MESSAGE ===');
    console.log('Input text:', inputText);

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date().toISOString(),
    };

    console.log('Created user message:', userMessage);
    
    // Add user message immediately using functional update
    setMessages(prevMessages => {
      const newMessages = [...prevMessages, userMessage];
      console.log('Updated messages state with user message:', newMessages);
      return newMessages;
    });
    
    // Clear input and show typing indicator
    setInputText('');
    setIsTyping(true);

    // Force scroll to bottom after user message
    setTimeout(() => {
      scrollToBottom();
    }, 50);

    // Update user stats
    if (user) {
      updateUser({ totalChats: (user.totalChats || 0) + 1 });
    }

    try {
      // Call the backend API
      const aiResponseText = await callBackendAPI(inputText);
      
      const aiResponse: ChatMessage = {
        id: (Date.now() + 1).toString(),
        text: aiResponseText,
        sender: 'ai',
        timestamp: new Date().toISOString(),
      };

      console.log('Created AI response:', aiResponse);
      
      // Append AI response using functional update
      setMessages(prevMessages => {
        const newMessages = [...prevMessages, aiResponse];
        console.log('Updated messages state with AI response:', newMessages);
        return newMessages;
      });
      
      // Force scroll to bottom after AI response
      setTimeout(() => {
        scrollToBottom();
      }, 100);
    } catch (error) {
      console.error('Error in handleSendMessage:', error);
      const errorResponse: ChatMessage = {
        id: (Date.now() + 1).toString(),
        text: 'I apologize, but I encountered an error while processing your message. Please try again.',
        sender: 'ai',
        timestamp: new Date().toISOString(),
      };
      
      // Append error response using functional update
      setMessages(prevMessages => [...prevMessages, errorResponse]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const copyLastAIResponse = () => {
    const lastAIMessage = messages.filter(msg => msg.sender === 'ai').pop();
    if (lastAIMessage) {
      navigator.clipboard.writeText(lastAIMessage.text);
      // Show a brief notification
      const notification = document.createElement('div');
      notification.textContent = 'Response copied to clipboard!';
      notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded shadow-lg z-50';
      document.body.appendChild(notification);
      setTimeout(() => document.body.removeChild(notification), 2000);
    }
  };

  const clearChat = async () => {
    if (window.confirm('Are you sure you want to clear the chat? This action cannot be undone.')) {
      try {
        // Clear messages from database
        const response = await fetch('http://127.0.0.1:8000/api/clear/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user_id: user?.id || 'anonymous',
            session_id: sessionId
          }),
        });

        if (response.ok) {
          // Start a new chat session
          startNewChat();
          
          // Show success notification
          const notification = document.createElement('div');
          notification.textContent = 'Chat cleared successfully!';
          notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded shadow-lg z-50';
          document.body.appendChild(notification);
          setTimeout(() => document.body.removeChild(notification), 2000);
        } else {
          throw new Error('Failed to clear chat');
        }
      } catch (error) {
        console.error('Error clearing chat:', error);
        const notification = document.createElement('div');
        notification.textContent = 'Error clearing chat. Please try again.';
        notification.className = 'fixed top-4 right-4 bg-red-500 text-white px-4 py-2 rounded shadow-lg z-50';
        document.body.appendChild(notification);
        setTimeout(() => document.body.removeChild(notification), 2000);
      }
    }
  };

  const formatSessionDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  console.log('Current messages state:', messages);
  console.log('Total messages count:', messages.length);
  console.log('Current session ID:', sessionId);

  return (
    <div className="bg-white border border-gray-200 rounded-2xl h-[600px] flex flex-col shadow-sm">
      {/* Chat Header */}
      <div className="flex items-center p-4 border-b border-gray-200">
        <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-r from-blue-600 to-indigo-700 rounded-full mr-3">
          <Bot className="h-6 w-6 text-white" />
        </div>
        <div>
          <h3 className="text-gray-900 font-semibold">AI Tutor</h3>
          <p className="text-gray-500 text-sm">Always ready to help you learn</p>
        </div>
        <div className="ml-auto flex items-center space-x-2">
          <Sparkles className="h-5 w-5 text-amber-500 animate-pulse" />
          {/* Debug info */}
          <div className="text-xs text-gray-400">
            Messages: {messages.length}
          </div>
          {/* Action buttons */}
          <button
            onClick={copyLastAIResponse}
            className="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
            title="Copy last AI response"
          >
            <Copy className="h-4 w-4" />
          </button>
          <button
            onClick={clearChat}
            className="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            title="Clear chat"
          >
            <Trash2 className="h-4 w-4" />
          </button>
          <button
            onClick={() => setShowSessions(!showSessions)}
            className="p-2 text-gray-500 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors"
            title="Previous chats"
          >
            <MessageSquare className="h-4 w-4" />
          </button>
          <button
            onClick={startNewChat}
            className="p-2 text-gray-500 hover:text-purple-600 hover:bg-purple-50 rounded-lg transition-colors"
            title="New chat"
          >
            <Plus className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Sessions Dropdown */}
      {showSessions && (
        <div className="border-b border-gray-200 p-4 bg-gray-50">
          <div className="flex items-center justify-between mb-2">
            <h4 className="text-sm font-medium text-gray-700">Previous Chats</h4>
            <button
              onClick={startNewChat}
              className="text-xs text-blue-600 hover:text-blue-700 font-medium"
            >
              + New Chat
            </button>
          </div>
          <div className="space-y-2 max-h-32 overflow-y-auto">
            {sessions.length > 0 ? (
              sessions.map((session) => (
                <button
                  key={session.session_id}
                  onClick={() => switchToSession(session.session_id)}
                  className={`w-full text-left p-2 rounded-lg text-xs transition-colors ${
                    session.session_id === sessionId
                      ? 'bg-blue-100 text-blue-700 border border-blue-200'
                      : 'hover:bg-gray-100 text-gray-600'
                  }`}
                >
                  <div className="flex justify-between items-center">
                    <span className="truncate">{formatSessionDate(session.created_at)}</span>
                    <span className="text-gray-400">{session.message_count} messages</span>
                  </div>
                </button>
              ))
            ) : (
              <p className="text-xs text-gray-500">No previous chats</p>
            )}
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => {
          console.log(`Rendering message ${index}:`, message);
          return (
            <ChatMessageComponent 
              key={message.id} 
              message={message} 
            />
          );
        })}
        {isTyping && <TypingIndicator />}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="flex-1 relative">
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything about learning..."
              className="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3 text-gray-900 placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all resize-none"
              rows={1}
              style={{ minHeight: '44px', maxHeight: '120px' }}
            />
          </div>
          <button
            onClick={handleSendMessage}
            disabled={!inputText.trim() || isTyping}
            className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white p-3 rounded-xl hover:from-blue-700 hover:to-indigo-800 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>
  );
}