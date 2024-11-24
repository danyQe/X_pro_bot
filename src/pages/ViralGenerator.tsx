import React, { useState } from 'react';
import axios from 'axios';
import { Sparkles, Loader2 } from 'lucide-react';

function ViralGenerator() {
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const generateThread = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:8000/viral');
      setResult(response.data.viral_tweets);
    } catch (error) {
      console.error('Error:', error);
      setResult('Error generating viral thread. Please try again.');
    }
    setLoading(false);
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

      {result && (
        <div className="mt-8 p-6 bg-white rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Generated Thread:</h2>
          <p className="text-gray-700 whitespace-pre-wrap">{result}</p>
        </div>
      )}
    </div>
  );
}

export default ViralGenerator;