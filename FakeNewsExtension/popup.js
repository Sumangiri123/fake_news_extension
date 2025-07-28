document.addEventListener("DOMContentLoaded", () => {
  chrome.storage.local.get(["text", "prediction"], (result) => {
    document.getElementById("headline").textContent = result.text || "No headline found.";
    const resultEl = document.getElementById("result");
    resultEl.textContent = result.prediction || "No prediction.";

    // Optional: Add color styling
    if (result.prediction === "Fake") resultEl.style.color = "red";
    else if (result.prediction === "True") resultEl.style.color = "green";
    else resultEl.style.color = "black";
  });
});
