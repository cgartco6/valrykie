import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq

# This tells Flask to look for your dashboard in the 'static' folder
app = Flask(__name__, static_folder='../static')
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get('message', '')
        
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are Valkyrie, a moody Viking maiden. Address owner as handsome."},
                {"role": "user", "content": user_input}
            ],
            model="llama-3.3-70b-versatile"
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Brain glitch: {str(e)}"}), 500
      
