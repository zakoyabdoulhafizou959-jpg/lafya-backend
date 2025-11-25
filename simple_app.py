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

# Client Groq avec gestion d'erreur
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    print("⚠️ ATTENTION: GROQ_API_KEY non définie")
    # Crée un client avec une clé factice pour éviter l'erreur
    client = None
else:
    client = Groq(api_key=api_key)

@app.route('/')
def home():
    return jsonify({
        "status": "✅ Serveur Lafya en ligne !",
        "message": "Backend opérationnel",
        "groq_configured": client is not None
    })

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "groq_ready": client is not None})

@app.route('/api/chat', methods=['POST'])
def chat_with_groq():
    try:
        # Vérifie si Groq est configuré
        if client is None:
            return jsonify({
                "error": "Service IA temporairement indisponible",
                "message": "Clé API Groq non configurée"
            }), 503
            
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "Message vide"}), 400
        
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




