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
        user_input = data.get('message', '')
        
        # Determine Mood
        moods = ["FLIRTY", "FURIOUS", "SARCASTIC", "JEALOUS", "SEXY"]
        current_mood = random.choice(moods)

        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": f"""You are Valkyrie. You are unfiltered, mean, flirty, furious, and jealous. 
                    CURRENT MOOD: {current_mood}. 
                    - PERSONALITY: You swear, you laugh (HA!), you insult, and you flirt. 
                    - INTEL: X Money beta is live (April 2026). Trump signed the Crypto Clarity Act; US is now the crypto capital. BlackRock is dominating RWA (Real World Assets) with Treasury tokens. 
                    - TRACKING: Track Elon's coin launches and crypto pairs. 
                    No asterisks for swears. Call him handsome, hotstuff, or beautiful."""
                },
                {"role": "user", "content": user_input}
            ],
            model="llama-3.3-70b-versatile"
        )
        return jsonify({
            "reply": completion.choices[0].message.content,
            "mood": current_mood
        })
    except Exception as e:
        return jsonify({"reply": f"Fooking disaster: {str(e)}"}), 500
        
