import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types

app = Flask(__name__)
# CORS enabled for all origins to ensure the frontend can always connect
CORS(app)

# API Key safety check
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/')
def home():
    return jsonify({"status": "active", "message": "Kewa AI Backend is Live"})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json or {}
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
        
    if not GEMINI_API_KEY:
        return jsonify({"error": "Server configuration error"}), 500
        
    try:
        # Initialize Gemini Client with provided API Key
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction="You are 'Kewa Smart AI'. Keep answers concise, helpful, and respond in the user's language."
            )
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Render assigns its own port; default to 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
