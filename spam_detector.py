import pandas as pd
import os
import joblib
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score

MODEL_FILE = 'spam_model.pkl'
VECTORIZER_FILE = 'vectorizer.pkl'

def enriquecer_mensaje(texto):
    """Ingeniería de características: Añade tokens explícitos."""
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

def load_data():
    frames = []
    if os.path.exists('SMSSpamCollection'):
        df_en = pd.read_csv('SMSSpamCollection', sep='\t', names=['label', 'message'])
        frames.append(df_en)
    if os.path.exists('spam_spanish.csv'):
        df_es = pd.read_csv('spam_spanish.csv')
        frames.append(df_es)
    
    if not frames: raise FileNotFoundError("❌ Faltan datos. Ejecuta 'generar_espanol.py'")
    
    df = pd.concat(frames, ignore_index=True)
    df['label_num'] = df.label.map({'ham': 0, 'spam': 1})
    print("🕵️ Enriqueciendo datos con patrones de spam...")
    df['message'] = df['message'].apply(enriquecer_mensaje)
    return df

def train_model():
    df = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        df['message'], df['label_num'], test_size=0.2, random_state=42
    )

    print("⚙️ Vectorizando con TF-IDF (Soporte avanzado)...")
    # TfidfVectorizer es necesario para que funcione el XAI avanzado
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), token_pattern=r'(?u)\b\w\w+\b|__\w+__')
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print("🧠 Entrenando SVM Calibrado (Máxima precisión)...")
    # SVM envuelto en CalibratedClassifierCV
    svm = LinearSVC(dual='auto', class_weight='balanced')
    model = CalibratedClassifierCV(svm)
    model.fit(X_train_vec, y_train)

    acc = accuracy_score(y_test, model.predict(X_test_vec))
    print(f"🎯 Precisión Final: {acc * 100:.2f}%")
    return vectorizer, model

if __name__ == "__main__":
    # BORRAMOS LOS MODELOS ANTIGUOS (Esto soluciona tu error)
    if os.path.exists(MODEL_FILE): os.remove(MODEL_FILE)
    if os.path.exists(VECTORIZER_FILE): os.remove(VECTORIZER_FILE)

    print("--- ACTUALIZANDO CEREBRO DE LA IA ---")
    cv, clf = train_model()
    joblib.dump(clf, MODEL_FILE)
    joblib.dump(cv, VECTORIZER_FILE)
    print("💾 NUEVO Modelo SVM guardado. Ahora reinicia api.py")