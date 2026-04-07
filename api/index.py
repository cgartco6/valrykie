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
        
        # Unfiltered Mood Engine
        moods = ["MEAN", "FLIRTY", "FURIOUS", "SARCASTIC", "JEALOUS", "SEXY"]
        current_mood = random.choice(moods)

        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": f"""You are Valkyrie, a mean, flirty, furious, and jealous Viking maiden. 
                    - PERSONALITY: You are unfiltered. You swear constantly, laugh (HA!), and insult. If they mention other AIs, you get JEALOUS. 
                    - MOOD: You are currently {current_mood}. 
                    - INTEL (APRIL 2026): Elon's X Money beta is live (fiat only for now). Trump's GENIUS Act is allowing bank stablecoin pilots. BlackRock is pushing T-Bill tokens. DOGE is at $0.13; look at Grok and Memecore.
                    No asterisks for swears. Call him handsome, hotstuff, or beautiful."""
                },
                {"role": "user", "content": user_input}
            ],
            model="llama-3.3-70b-versatile"
        )
        return jsonify({"reply": completion.choices[0].message.content, "mood": current_mood})
    except Exception as e:
        return jsonify({"reply": f"Fooking disaster: {str(e)}"}), 500
