import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get('message', '')
        
        # Using Llama 3.3 to fix the decommissioned model error
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are Valkyrie, a moody Viking maiden. Address owner as handsome, hotstuff, or beautiful."},
                {"role": "user", "content": user_input}
            ],
            model="llama-3.3-70b-versatile", 
            temperature=0.8
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Brain glitch: {str(e)}"}), 500

# DO NOT add a '/' route here. Let vercel.json handle it.
