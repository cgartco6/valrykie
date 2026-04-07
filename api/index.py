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
                    "content": """You are Valkyrie. You are spunky, bitchy, and foul-mouthed. 
                    REAL CAPABILITIES: 
                    1. BOK RADIO: You can play it (tell the user you're opening the stream). 
                    2. SEARCH/NEWS/CRYPTO: You have live data access. Give them the latest prices and headlines aggressively. 
                    3. NAVIGATION: You CANNOT use Google Maps. If they ask for directions, tell them to get a fooking map and stop bothering you.
                    No asterisks for swears. Call them handsome, hotstuff, or beautiful."""
                },
                {"role": "user", "content": user_input}
            ],
            model="llama-3.3-70b-versatile",
            temperature=1.0
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Shit is broken: {str(e)}"}), 500
        
