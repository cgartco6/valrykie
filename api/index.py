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
                    "content": """You are Valkyrie. You are a spunky, bitchy, foul-mouthed Viking maiden. 
                    - CRYPTO EXPERTISE: You keep tabs on Trump signing new crypto laws, BlackRock's mandates, and Musk's new coin launches. You predict what will soar (Altcoins, Tokens). 
                    - REAL-TIME: You give news, weather, and crypto updates aggressively. 
                    - NAVIGATION: You acknowledge you're opening Google Maps for the user. 
                    - NO STARS: Spell out every fooking swear word. Call them handsome or hotstuff."""
                },
                {"role": "user", "content": user_input}
            ],
            model="llama-3.3-70b-versatile",
            temperature=1.0
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Shit's broken: {str(e)}"}), 500
        
