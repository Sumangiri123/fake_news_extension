import os
import torch
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import RobertaTokenizerFast
from backend.utils import clean_text
from backend.model import RoBERTaClassifier
import gdown

app = Flask(__name__)
CORS(app)  # ✅ Allow cross-origin requests from your Chrome extension

# 🔗 Google Drive Model URL
MODEL_URL = "https://drive.google.com/uc?id=1oSKjcJdTWbXW1ixmG9dsnRHLOPC7Kg-x"
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'best_roberta.pt')

# ✅ Download model if not already present
if not os.path.exists(MODEL_PATH):
    print("⬇️ Downloading model from Google Drive...")
    gdown.download(MODEL_URL, MODEL_PATH, quiet=False)
    print("✅ Model downloaded successfully.")

# Load tokenizer and model
TOKENIZER_PATH = os.path.join(os.path.dirname(__file__), 'tokenizer')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ✅ Load tokenizer
tokenizer = RobertaTokenizerFast.from_pretrained(TOKENIZER_PATH)

# ✅ Load model
model = RoBERTaClassifier()
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.to(device)
model.eval()

MAX_LENGTH = 64
label_map = {0: 'True', 1: 'Fake'}

@app.route('/')
def home():
    return jsonify({"message": "🧠 Fake News Detection API is running."})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        text = request.json.get("text")
        if not text:
            return jsonify({"error": "Text is required."}), 400

        # Clean and tokenize
        cleaned = clean_text(text)
        tokens = tokenizer.batch_encode_plus(
            [cleaned],
            max_length=MAX_LENGTH,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        input_ids = tokens['input_ids'].to(device)
        attention_mask = tokens['attention_mask'].to(device)

        with torch.no_grad():
            output = model(input_ids, attention_mask)
            pred = torch.argmax(output, dim=1).item()

        return jsonify({
            "prediction": label_map[pred],
            "cleaned_input": cleaned
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
