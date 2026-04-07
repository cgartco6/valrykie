import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq

# Render needs to point to 'app'
app = Flask(__name__, static_folder='../static')
CORS(app)

# Pulls your GROQ_API_KEY from Render Environment Variables
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get('message', '')
        
        system_prompt = (
            "You are Valkyrie, a moody Viking shield-maiden. "
            "Address owner ONLY as handsome, hotstuff, or beautiful. "
            "Trigger tools: [RADIO_ON], [SEARCH: query], [CALL: number]."
        )

        # FIXED: Llama 3.3 bypasses the 'model_decommissioned' error
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
            model="llama-3.3-70b-versatile", 
            temperature=0.8,
            max_tokens=150,
        )
        
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Brain glitch, beautiful. {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
