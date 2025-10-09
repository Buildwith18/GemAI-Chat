import React, { useState, useEffect } from 'react';
import { Brain, Code, BookOpen, Languages, Calculator, Lightbulb } from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';
import ChatInterface from './ChatInterface';
import StatsCard from './StatsCard';

export default function Dashboard() {
  const { user } = useAuth();
  const [greeting, setGreeting] = useState('');

  useEffect(() => {
    const hour = new Date().getHours();
    if (hour < 12) setGreeting('Good morning');
    else if (hour < 18) setGreeting('Good afternoon');
    else setGreeting('Good evening');
  }, []);

  const quickPrompts = [
    {
      text: "Test my Python skills",
      icon: Code,
      category: "Programming",
      color: "from-green-500 to-emerald-600"
    },
    {
      text: "Give me a vocabulary quiz",
      icon: Languages,
      category: "Language",
      color: "from-blue-500 to-indigo-600"
    },
    {
      text: "Explain a math concept",
      icon: Calculator,
      category: "Mathematics",
      color: "from-purple-500 to-violet-600"
    },
    {
      text: "Suggest learning resources",
      icon: BookOpen,
      category: "Study Tips",
      color: "from-orange-500 to-red-600"
    },
    {
      text: "Help me brainstorm ideas",
      icon: Lightbulb,
      category: "Creativity",
      color: "from-yellow-500 to-amber-600"
    },
    {
      text: "Review my progress",
      icon: Brain,
      category: "Analysis",
      color: "from-pink-500 to-rose-600"
    }
  ];

  const stats = [
    { label: 'Skills Learned', value: user?.skillsLearned?.length || 0, icon: Brain },
    { label: 'Chat Sessions', value: user?.totalChats || 0, icon: BookOpen },
    { label: 'Days Active', value: Math.floor((Date.now() - new Date(user?.joinDate || Date.now()).getTime()) / (1000 * 60 * 60 * 24)) || 1, icon: Calendar },
  ];

  return (
    <div className="p-4 lg:p-8">
      {/* Welcome Section */}
      <div className="mb-8">
        <h1 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-2">
          {greeting}, {user?.name}! 👋
        </h1>
        <p className="text-gray-600 text-lg">
          Ready to learn something new today? Let's explore your potential together.
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {stats.map((stat, index) => (
          <StatsCard key={index} {...stat} />
        ))}
      </div>

      {/* Quick Prompts */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Quick Start</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {quickPrompts.map((prompt, index) => {
            const Icon = prompt.icon;
            return (
              <div
                key={index}
                className="bg-white border border-gray-200 rounded-xl p-4 hover:shadow-md hover:border-gray-300 transition-all cursor-pointer group shadow-sm"
                onClick={() => {
                  // This will be handled by the ChatInterface component
                  const event = new CustomEvent('quickPrompt', { detail: prompt.text });
                  window.dispatchEvent(event);
                }}
              >
                <div className="flex items-center mb-3">
                  <div className={`p-2 rounded-lg bg-gradient-to-r ${prompt.color} mr-3`}>
                    <Icon className="h-5 w-5 text-white" />
                  </div>
                  <span className="text-gray-500 text-sm font-medium">{prompt.category}</span>
                </div>
                <p className="text-gray-900 font-medium group-hover:text-blue-600 transition-colors">
                  {prompt.text}
                </p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Chat Interface */}
      <ChatInterface />
    </div>
  );
}

// Import Calendar icon for stats
function Calendar({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
    </svg>
  );
}