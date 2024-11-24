import React, { useState } from 'react';
import axios from 'axios';
import { CheckCircle, Loader2 } from 'lucide-react';

function FactChecker() {
  const [tweet, setTweet] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/facts', { tweet });
      setResult(response.data.Fact_description);
    } catch (error) {
      console.error('Error:', error);
      setResult('Error checking facts. Please try again.');
    }
    setLoading(false);
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-12">
      <div className="text-center mb-8">
        <CheckCircle className="h-12 w-12 text-green-500 mx-auto mb-4" />
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Fact Checker</h1>
        <p className="text-gray-600">Verify the accuracy of any tweet</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <textarea
            value={tweet}
            onChange={(e) => setTweet(e.target.value)}
            placeholder="Enter the tweet to fact-check..."
            className="w-full h-32 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-green-500 text-white py-3 px-6 rounded-lg font-medium hover:bg-green-600 transition-colors disabled:bg-green-300 flex items-center justify-center"
        >
          {loading ? (
            <>
              <Loader2 className="animate-spin h-5 w-5 mr-2" />
              Checking Facts...
            </>
          ) : (
            'Check Facts'
          )}
        </button>
      </form>

      {result && (
        <div className="mt-8 p-6 bg-white rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Results:</h2>
          <p className="text-gray-700 whitespace-pre-wrap">{result}</p>
        </div>
      )}
    </div>
  );
}

export default FactChecker;