import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq

# Set the static folder explicitly
app = Flask(__name__, static_folder='../static')
CORS(app)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ROUTE 1: Serve the HTML dashboard
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# ROUTE 2: MANUALLY SERVE IMAGES (This fixes the 'Not Loading' issue)
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get('message', '')
        
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "You are Valkyrie. You are spunky, bitchy, and foul-mouthed. Use phonetic swears. You track Trump crypto laws, Elon Musk coin launches, and BlackRock mandates. Address user as handsome or hotstuff."
                },
                {"role": "user", "content": user_input}
            ],
            model="llama-3.3-70b-versatile",
            temperature=1.0
        )
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Fooking error: {str(e)}"}), 500
