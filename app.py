from flask import Flask, render_template_string, request, jsonify
from google import genai
import os

# Render par current folder se hi HTML uthane ke liye path setting
current_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(current_dir, 'index.html')

# Gemini API Configuration
API_KEY = "AIzaSyCCJ2zyArvJhQQafFSBxQCP4MALwnBWXTU"
model_name = 'gemini-2.5-flash'

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    print(f"Gemini Client Error: {e}")
    client = None

app = Flask(__name__)

# 1. Yeh tumhara main route hai jo Sunder HTML page dikhayega!
@app.route('/')
def home():
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return render_template_string(html_content)
    except Exception as e:
        return f"Error: 'index.html' file nahi mili server par: {str(e)}"

# 2. Yeh backend API hai chat ke liye
@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    if not user_input:
        return jsonify({'response': "Bhai kuch toh bolo!"})

    if not client:
        return jsonify({'response': f"[MOCK] Aapne kaha: '{user_input}'"})

    try:
        response = client.models.generate_content(model=model_name, contents=user_input)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'response': f"Oops! API Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
    
