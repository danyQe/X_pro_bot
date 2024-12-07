// Listen for installation
chrome.runtime.onInstalled.addListener(() => {
    console.log('XLENS Extension installed');
  });
  
  // Listen for messages from content script
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'ANALYZE_TWEET') {
        analyzeTweet(request.data)
            .then(response => sendResponse(response))
            .catch(error => {
                console.error('Analysis error:', error);
                sendResponse({ error: error.message });
            });
        return true;
    }
});
  
  async function analyzeTweet(tweetData: string) {
    // Make API call to local server
    const response = await fetch('http://localhost:8000/facts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ tweet: tweetData }),
    });
    return response.json();
  }