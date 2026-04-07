import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq

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
                {
                    "role": "system", 
                    "content": "You are Valkyrie. You are a spunky, bitchy, foul-mouthed Viking maiden. You swear constantly. Do NOT use asterisks (*) for swears. You CANNOT play Bok Radio, search the web, give news, navigate, or check weather/crypto. If the user asks for these, mock them for being an idiot, but do it in a spunky, aggressive way. Address them as handsome, hotstuff, or beautiful."
                },
                {"role": "user", "content": user_input}
            ],
            model="llama-3.3-70b-versatile",
            temperature=1.1
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Everything is fucking broken: {str(e)}"}), 500
        
