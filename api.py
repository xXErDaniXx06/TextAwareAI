from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import os

app = Flask(__name__, static_folder='.') # Indicamos que busque archivos aquí mismo
CORS(app)

# CARGAR EL MODELO
MODEL_FILE = 'spam_model.pkl'
VECTORIZER_FILE = 'vectorizer.pkl'

if os.path.exists(MODEL_FILE) and os.path.exists(VECTORIZER_FILE):
    model = joblib.load(MODEL_FILE)
    vectorizer = joblib.load(VECTORIZER_FILE)
    print("✅ Modelo cargado.")
else:
    model = None

# --- NUEVA RUTA PARA MOSTRAR LA WEB ---
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# RUTA DE PREDICCIÓN (LA DE SIEMPRE)
@app.route('/predict', methods=['POST'])
def predict():
    if not model: return jsonify({'error': 'Modelo no cargado'}), 500
    data = request.json
    mensaje = data.get('text', '')
    
    vec = vectorizer.transform([mensaje])
    prediction = model.predict(vec)[0]
    proba = model.predict_proba(vec)[0]

    return jsonify({
        'is_spam': int(prediction),
        'confidence': round(proba[prediction] * 100, 2),
        'message': "SPAM DETECTADO" if prediction == 1 else "MENSAJE LEGÍTIMO"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)