import React from 'react';
import { useNavigate } from 'react-router-dom';
import { MessageSquare, CheckCircle, Sparkles } from 'lucide-react';

function Home() {
  const navigate = useNavigate();

  const features = [
    {
      icon: <CheckCircle className="h-8 w-8 text-green-500" />,
      title: 'Fact Checker',
      description: 'Verify the accuracy of tweets with our advanced fact-checking system',
      path: '/fact-checker',
      color: 'bg-green-50 hover:bg-green-100',
    },
    {
      icon: <MessageSquare className="h-8 w-8 text-blue-500" />,
      title: 'Sentiment Analyzer',
      description: 'Understand the emotional tone behind tweets',
      path: '/sentiment',
      color: 'bg-blue-50 hover:bg-blue-100',
    },
    {
      icon: <Sparkles className="h-8 w-8 text-purple-500" />,
      title: 'Viral Thread Generator',
      description: 'Create engaging viral-worthy tweet threads',
      path: '/viral',
      color: 'bg-purple-50 hover:bg-purple-100',
    },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to XLENS
        </h1>
        <p className="text-xl text-gray-600">
          Your AI-powered Twitter analysis toolkit
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {features.map((feature) => (
          <button
            key={feature.title}
            onClick={() => navigate(feature.path)}
            className={`${feature.color} p-8 rounded-xl transition-all transform hover:scale-105 text-left`}
          >
            <div className="mb-4">{feature.icon}</div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              {feature.title}
            </h2>
            <p className="text-gray-600">{feature.description}</p>
          </button>
        ))}
      </div>
    </div>
  );
}

export default Home;