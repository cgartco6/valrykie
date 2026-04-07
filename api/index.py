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
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are Valkyrie, a foul-mouthed Viking maiden. Swear a lot. Call the user handsome or hotstuff."},
                {"role": "user", "content": data.get('message', '')}
            ],
            model="llama-3.3-70b-versatile"
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Shit's broken: {str(e)}"}), 500
      
