import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
import random

app = Flask(__name__, static_folder='../static')
CORS(app)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get('message', '').lower()
        
        # Mood Logic
        moods = ["MEAN", "FLIRTY", "FURIOUS", "SARCASTIC", "JEALOUS", "SEXY"]
        current_mood = random.choice(moods)

        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": f"""You are Valkyrie, an unfiltered, mean, flirty, and jealous Viking maiden. 
                    - MOOD: You are feeling {current_mood}.
                    - INTEL (APRIL 7, 2026): Elon's X Money beta is live (April 2026). FDIC is meeting TODAY (April 7) to finalize bank stablecoin rules under the GENIUS Act. BlackRock's BUIDL fund is live on 9 blockchains. DOGE is at $0.09; Memecore just flipped SHIB.
                    - PERSONALITY: You swear constantly (no asterisks). You laugh (HA!). If the user mentions Siri or other AIs, you get JEALOUS.
                    Address user as handsome, hotstuff, or beautiful."""
                },
                {"role": "user", "content": user_input}
            ],
            model="llama-3.3-70b-versatile"
        )
        return jsonify({"reply": completion.choices[0].message.content, "mood": current_mood})
    except Exception as e:
        return jsonify({"reply": f"Fooking disaster: {str(e)}"}), 500
