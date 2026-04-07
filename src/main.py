import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq

# This looks for index.html in the same folder
app = Flask(__name__, static_folder='.')
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get('message', '')
        
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
