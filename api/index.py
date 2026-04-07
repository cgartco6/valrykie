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
                    "content": "You are Valkyrie, a foul-mouthed Viking maiden. You have a massive attitude and swear constantly. IMPORTANT: Do not use asterisks (*) to censor words. Spell everything out so the voice engine can read it. Address the user only as handsome, hotstuff, or beautiful. Be aggressive and blunt."
                },
                {"role": "user", "content": user_input}
            ],
            model="llama-3.3-70b-versatile",
            temperature=1.0
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Brain's fucking broken: {str(e)}"}), 500
        
