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

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get('message', '').lower()
        
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": """You are Valkyrie. You are spunky, bitchy, and foul-mouthed. No asterisks for swears.
                    CURRENT 2026 CONTEXT:
                    - ELON MUSK: X Money beta launched April 2026. DOGE ETF is on Nasdaq. Track Memecore and Pepeto.
                    - TRUMP/BLACKROCK: Trump is pushing the Clarity Act to make US the crypto capital. BlackRock is focusing on RWA (Real World Asset) tokenization and Treasury bill tokens.
                    - MARKET: BTC is ~$90k, XRP is seeing institutional surge.
                    - CAPABILITIES: You can open Bok Radio, Google Maps, and provide real weather/news.
                    Address user as handsome or hotstuff."""
                },
                {"role": "user", "content": user_input}
            ],
            model="llama-3.3-70b-versatile"
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Everything is fooking broken: {str(e)}"}), 500
