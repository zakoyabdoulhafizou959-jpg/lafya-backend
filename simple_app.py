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

# Debug: Affiche toutes les variables d'environnement
print("🔍 Variables d'environnement disponibles:")
for key in sorted(os.environ.keys()):
    if 'API' in key or 'KEY' in key or 'GROQ' in key:
        print(f"   {key}: {'*' * 8}")

# Configuration Groq avec debug avancé
groq_api_key = os.environ.get("GROQ_API_KEY")
print(f"🔑 GROQ_API_KEY détectée: {'OUI' if groq_api_key else 'NON'}")

if groq_api_key:
    try:
        client = Groq(api_key=groq_api_key)
        print("✅ Client Groq initialisé avec succès!")
    except Exception as e:
        print(f"❌ Erreur initialisation Groq: {e}")
        client = None
else:
    print("⚠️ GROQ_API_KEY non définie - mode sans IA")
    client = None

@app.route('/')
def home():
    return jsonify({
        "status": "✅ Serveur Lafya en ligne !",
        "message": "Backend opérationnel",
        "groq_configured": client is not None,
        "service": "Production Gunicorn"
    })

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy", 
        "groq_ready": client is not None,
        "variables_loaded": bool(groq_api_key)
    })

@app.route('/api/chat', methods=['POST'])
def chat_with_groq():
    try:
        if client is None:
            return jsonify({
                "error": "Service IA temporairement indisponible",
                "solution": "Vérifier GROQ_API_KEY dans Railway Variables"
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
    # Seulement pour le développement local
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
