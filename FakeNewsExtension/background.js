chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "checkFakeNews",
    title: "Check if this is Fake News",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "checkFakeNews") {
    chrome.storage.local.set({ text: info.selectionText, prediction: "Checking..." }, () => {
      chrome.tabs.sendMessage(tab.id, { action: "analyzeSelectedText" });
    });
  }
});
