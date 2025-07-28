# 📰 Fake News Detection Project

This project detects fake news headlines using a fine-tuned RoBERTa model and deploys it via:

- 🔥 Flask API (`/backend`)
- ⚙️ Chrome Extension (`/extension`) for real-time usage

---

## 🔧 Project Structure

FakeNewsDetectionProject/
│
├── backend/ ← Flask REST API for predictions
│ ├── app.py ← Flask server code
│ ├── roberta_model_weights.pt
│ ├── tokenizer/ ← Tokenizer files
│ ├── utils.py
│ ├── model.py
│ ├── requirements.txt
│
├── extension/ ← Chrome Extension files
│ ├── manifest.json
│ ├── background.js
│ ├── content.js
│ ├── popup.html
│ ├── popup.js
│ └── style.css
│
├── datasets/ ← Raw datasets (optional)
│ ├── a1_True.csv
│ └── a2_Fake.csv
│
├── README.md ← This file
└── .gitignore ← Files to exclude from Git