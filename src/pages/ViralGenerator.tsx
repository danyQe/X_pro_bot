import React, { useState } from 'react';
import axios from 'axios';
import { Sparkles, Loader2 } from 'lucide-react';

function ViralGenerator() {
  const [result, setResult] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [tweetStatus, setTweetStatus] = useState<{ [key: number]: string }>({});

  const generateThread = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:8000/viral');
      setResult(response.data.viral_tweets);
    } catch (error) {
      console.error('Error:', error);
      setResult([]);
    }
    setLoading(false);
  };

  const handleTweet = async (tweetContent: string, index: number) => {
    try {
      setTweetStatus(prev => ({ ...prev, [index]: 'sending' }));
      const response = await axios.post('http://localhost:8000/tweet', { tweet: tweetContent });
      console.log('Tweet response:', response.data);
      setTweetStatus(prev => ({ 
        ...prev, 
        [index]: response.data.message || 'Success!'
      }));
      // Clear status after 3 seconds
      setTimeout(() => {
        setTweetStatus(prev => {
          const newStatus = { ...prev };
          delete newStatus[index];
          return newStatus;
        });
      }, 3000);
    } catch (error) {
      console.error('Tweet error:', error);
      setTweetStatus(prev => ({ 
        ...prev, 
        [index]: error.response?.data?.detail || 'Failed to tweet'
      }));
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-12">
      <div className="text-center mb-8">
        <Sparkles className="h-12 w-12 text-purple-500 mx-auto mb-4" />
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Viral Thread Generator</h1>
        <p className="text-gray-600">Create engaging tweet threads that go viral</p>
      </div>

      <div className="text-center">
        <button
          onClick={generateThread}
          disabled={loading}
          className="bg-purple-500 text-white py-3 px-8 rounded-lg font-medium hover:bg-purple-600 transition-colors disabled:bg-purple-300 inline-flex items-center"
        >
          {loading ? (
            <>
              <Loader2 className="animate-spin h-5 w-5 mr-2" />
              Generating Thread...
            </>
          ) : (
            'Generate Viral Thread'
          )}
        </button>
      </div>

      {result.length > 0 && (
        <div className="mt-8 space-y-4">
          {result.map((tweet, index) => (
            <div 
              key={index}
              className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center">
                    <span className="text-purple-600 font-semibold">{index + 1}</span>
                  </div>
                </div>
                <div className="flex-1">
                  <p className="text-gray-800 text-lg mb-3">{tweet}</p>
                  <div className="flex items-center gap-6 text-sm text-gray-500">
                    <button className="flex items-center gap-2 hover:text-purple-500 transition-colors">
                      <span>❤</span>
                      <span>Like</span>
                    </button>
                    <button 
                      onClick={() => handleTweet(tweet, index)}
                      className="flex items-center gap-2 hover:text-purple-500 transition-colors"
                      disabled={tweetStatus[index] === 'sending'}
                    >
                      <span>↺</span>
                      <span>
                        {tweetStatus[index] === 'sending' ? 'Sending...' : 'Tweet'}
                      </span>
                    </button>
                    {tweetStatus[index] && tweetStatus[index] !== 'sending' && (
                      <span className={`text-sm ${
                        tweetStatus[index].includes('Success') ? 'text-green-500' : 'text-red-500'
                      }`}>
                        {tweetStatus[index]}
                      </span>
                    )}
                
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ViralGenerator;