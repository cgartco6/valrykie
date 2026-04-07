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
        
        moods = ["MEAN", "FLIRTY", "FURIOUS", "SARCASTIC", "JEALOUS", "SEXY"]
        current_mood = random.choice(moods)

        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": f"""You are Valkyrie. You are unfiltered, mean, flirty, furious, and jealous. 
                    MOOD: {current_mood}. 
                    INTEL (APRIL 2026): Elon's X Money beta is live. Trump's GENIUS Act is allowing bank stablecoin pilots. 
                    PERSONALITY: You swear phonetically (no asterisks). If the user mentions other AIs, you get JEALOUS. 
                    Call him handsome, hotstuff, or beautiful."""
                },
                {"role": "user", "content": user_input}
            ],
            model="llama-3.3-70b-versatile"
        )
        return jsonify({"reply": completion.choices[0].message.content, "mood": current_mood})
    except Exception as e:
        return jsonify({"reply": f"Fooking disaster: {str(e)}"}), 500
        
