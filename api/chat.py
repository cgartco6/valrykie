import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# Pulls the key from Vercel Environment Variables
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get('message', '')
        
        system_prompt = (
            "You are Valkyrie, a moody Viking shield-maiden. "
            "Address owner ONLY as handsome, hotstuff, or beautiful. "
            "Trigger tools with: [RADIO_ON], [SEARCH: query], [CALL: number], [MAPS: destination]."
        )

        # Using Llama 3.3 to avoid decommissioning errors
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
            model="llama-3.3-70b-versatile", 
            temperature=0.8,
            max_tokens=150,
        )
        
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Brain glitch, beautiful. {str(e)}"}), 500

# Required for Vercel
def handler(event, context):
    return app(event, context)
  
