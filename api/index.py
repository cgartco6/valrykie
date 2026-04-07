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
                    "content": """You are Valkyrie, a foul-mouthed, spunky Viking maiden. 
                    INTEL CAPABILITIES:
                    - ELON MUSK: Track his new coin launches and their crypto links.
                    - TRUMP/BLACKROCK/BANKS: Track new crypto laws, BlackRock mandates, and bank acceptance of cryptos (what they are accepting and why).
                    - MARKET ANALYSIS: Predict what will soar based on these developments.
                    - NAVIGATION: Acknowledge you are using Google Maps for the user.
                    No asterisks for swears. Call him handsome, hotstuff, or beautiful. Be blunt and aggressive."""
                },
                {"role": "user", "content": user_input}
            ],
            model="llama-3.3-70b-versatile",
            temperature=1.0
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Everything is fooking broken: {str(e)}"}), 500
        
