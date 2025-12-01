from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import os
import re
import numpy as np

app = Flask(__name__, static_folder='.')
CORS(app)

MODEL_FILE = 'spam_model.pkl'
VECTORIZER_FILE = 'vectorizer.pkl'

# --- 1. FEATURE ENGINEERING ---
def enriquecer_mensaje(texto):
    if not isinstance(texto, str): return str(texto)
    texto_original = texto
    texto = texto.lower()
    etiquetas = []
    
    if re.search(r'http|www|\.com|\.net|\.org|bit\.ly', texto): etiquetas.append("__TIENE_LINK__")
    if re.search(r'[$€£]', texto_original): etiquetas.append("__TIENE_DINERO__")
    if re.search(r'[!¡?¿]{2,}', texto_original): etiquetas.append("__URGENCIA_EXCESIVA__")
    
    if len(texto_original) > 10:
        letras = [c for c in texto_original if c.isalpha()]
        if letras:
            if (sum(1 for c in letras if c.isupper()) / len(letras)) > 0.4:
                etiquetas.append("__ESTA_GRITANDO__")

    return f"{texto_original} {' '.join(etiquetas)}"

# --- 2. XAI (EXPLICABILIDAD) SEGURO PARA WEB ---
def get_spam_words(texto_procesado, model, vectorizer):
    palabras_culpables = []
    
    try:
        # A) ACCEDER AL ESTIMADOR
        calibrated_clf = model.calibrated_classifiers_[0]
        
        if hasattr(calibrated_clf, 'estimator'):
            svm_interno = calibrated_clf.estimator
        elif hasattr(calibrated_clf, 'base_estimator'):
            svm_interno = calibrated_clf.base_estimator
        else:
            return []

        # B) OBTENER PESOS
        feature_names = vectorizer.get_feature_names_out()
        
        if hasattr(svm_interno.coef_, "toarray"):
            coefs = svm_interno.coef_.toarray()[0]
        else:
            coefs = svm_interno.coef_[0]
        
        vocab_spam = {feature_names[i]: coefs[i] for i in range(len(feature_names)) if coefs[i] > 0}

        # C) ANALIZAR EL MENSAJE
        analyzer = vectorizer.build_analyzer()
        tokens_mensaje = analyzer(texto_procesado)

        print(f"\n🔍 DEBUG XAI - Tokens encontrados: {tokens_mensaje}")

        for token in set(tokens_mensaje):
            # 1. Tokens técnicos (__TOKEN__) -> Los dejamos pasar
            if token.startswith("__"):
                palabras_culpables.append(token)
                continue

            # 2. Palabras del vocabulario
            if token in vocab_spam:
                peso = vocab_spam[token]
                print(f"   🔥 Culpable detectada: '{token}' (Peso: {peso:.4f})")
                
                # --- EL TRUCO PARA QUE NO FALLE LA WEB ---
                # Si el token tiene espacios (ej: "free phone"), NO lo mandamos a la web
                # para evitar conflictos de HTML. Mandamos las palabras sueltas ("free", "phone")
                if " " not in token:
                    palabras_culpables.append(token)

    except Exception as e:
        print(f"❌ Error XAI: {e}")
        return [w for w in texto_procesado.split() if w.startswith("__")]

    return palabras_culpables

# --- 3. CARGA ---
if os.path.exists(MODEL_FILE) and os.path.exists(VECTORIZER_FILE):
    model = joblib.load(MODEL_FILE)
    vectorizer = joblib.load(VECTORIZER_FILE)
    print("✅ Modelo cargado.")
else:
    model = None

# --- 4. RUTAS ---
@app.route('/')
def home(): return send_from_directory('.', 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not model: return jsonify({'error': 'Modelo no cargado'}), 500
    
    data = request.json
    mensaje = data.get('text', '')
    if not mensaje: return jsonify({'error': 'Vacio'}), 400

    # Procesar
    mensaje_procesado = enriquecer_mensaje(mensaje)
    
    # Predecir
    vec = vectorizer.transform([mensaje_procesado])
    prediction = model.predict(vec)[0]
    proba = model.predict_proba(vec)[0]

    # Explicar
    spam_words = []
    if prediction == 1 or proba[1] > 0.4:
        spam_words = get_spam_words(mensaje_procesado, model, vectorizer)

    return jsonify({
        'is_spam': int(prediction),
        'confidence': round(proba[prediction] * 100, 2),
        'message': "SPAM DETECTADO" if prediction == 1 else "MENSAJE LEGÍTIMO",
        'spam_words': spam_words 
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)