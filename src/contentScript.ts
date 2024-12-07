/// <reference path="../node_modules/@types/chrome/index.d.ts" />

// Listen for tweets and add XLENS buttons
function addXLensButtons() {
    const tweets = document.querySelectorAll('article[data-testid="tweet"]');
    tweets.forEach(tweet => {
      if (!tweet.querySelector('.xlens-button')) {
        const button = document.createElement('button');
        button.className = 'xlens-button';
        button.textContent = 'Analyze with XLENS';
        button.onclick = () => analyzeTweet(tweet);
        tweet.appendChild(button);
      }
    });
  }
  
  function analyzeTweet(tweetElement: Element) {
    const tweetText = tweetElement.querySelector('[data-testid="tweetText"]')?.textContent;
    if (tweetText) {
      // Add error handling for empty or invalid tweet text
      if (!tweetText.trim()) {
        showAnalysisResult({ error: 'No tweet text found' }, tweetElement);
        return;
      }

      chrome.runtime.sendMessage(
        { 
          type: 'ANALYZE_TWEET', 
          data: {
            tweet: tweetText.trim() // Ensure proper data structure
          }
        },
        (response: any) => {
          showAnalysisResult(response, tweetElement);
        }
      );
    }
  }
  
  function showAnalysisResult(result: any, tweetElement: Element) {
    const resultDiv = document.createElement('div');
    resultDiv.className = 'xlens-result';
    resultDiv.textContent = result.Fact_description || result.error;
    tweetElement.appendChild(resultDiv);
  }
  
  // Start observing for new tweets
  const observer = new MutationObserver(() => {
    addXLensButtons();
  });
  
  observer.observe(document.body, {
    childList: true,
    subtree: true,
  });
  
  addXLensButtons();