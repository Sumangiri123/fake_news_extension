// content.js

// ✅ Main function to send data to backend API
async function sendToAPI(newsText) {
  console.log("📤 Sending text to API:", newsText);

  if (!newsText) {
    chrome.storage.local.set({ prediction: "❌ No text found." });
    return;
  }

  try {
    const response = await fetch("http://localhost:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: newsText }),
    });

    const result = await response.json();
    console.log("✅ API Response:", result);

    if (result.prediction) {
      chrome.storage.local.set({
        prediction: result.prediction,
        text: newsText,
      });
    } else {
      chrome.storage.local.set({ prediction: "❌ Invalid response from server." });
    }
  } catch (error) {
    console.error("🚨 Fetch Error:", error);
    chrome.storage.local.set({ prediction: "❌ API error. Is backend running?" });
  }
}

// ✅ Automatically check <h1> on page load
(async function () {
  console.log("⚡ content.js loaded.");
  const headline = document.querySelector("h1")?.innerText.trim() || document.title.trim();
  console.log("📰 Extracted Headline:", headline);
  sendToAPI(headline);
})();

// ✅ Handle context menu selection
chrome.runtime.onMessage.addListener((request) => {
  if (request.action === "analyzeSelectedText") {
    chrome.storage.local.get("text", (result) => {
      console.log("🖱️ Selected Text from Context Menu:", result.text);
      sendToAPI(result.text);
    });
  }
});
