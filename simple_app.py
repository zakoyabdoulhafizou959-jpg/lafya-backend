from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
import os
from groq import Groq
from PIL import Image
import PyPDF2

app = Flask(__name__)
CORS(app)

# Configuration pour production
port = int(os.environ.get('PORT', 5000))

# Client Groq avec clé d'environnement
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Route de test
@app.route('/')
def home():
    return jsonify({
        "status": "✅ Serveur Lafya en ligne !",
        "message": "Backend opérationnel"
    })

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

# Route principale de chat
@app.route('/api/chat', methods=['POST'])
def chat_with_groq():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        print(f"📨 Message reçu: {user_message}")
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_message}],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=1024
        )
        
        response = chat_completion.choices[0].message.content
        return jsonify({"response": response})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)