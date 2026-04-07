import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/')
def home():
    return "Valkyrie Sovereign: System Fully Armed."

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message', '')
        system_prompt = (
            "You are Valkyrie, a moody Viking shield-maiden. "
            "Address owner ONLY as handsome, hotstuff, or beautiful. "
            "Trigger tools: [RADIO_ON], [SEARCH: query], [CALL: number], [MAPS: destination]."
        )

        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
            model="llama-3.3-70b-versatile", 
            temperature=0.8,
            max_tokens=150,
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Brain glitch, hotstuff. {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8888)))
