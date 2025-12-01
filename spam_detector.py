import pandas as pd
import os
import joblib  # Esta es la librería para guardar/cargar la "memoria"
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Archivos donde guardaremos el cerebro de la IA
MODEL_FILE = 'spam_model.pkl'
VECTORIZER_FILE = 'vectorizer.pkl'

def load_data_bilingue():
    """Carga datos de inglés y español y los junta."""
    frames = []
    
    # 1. Cargar Inglés
    if os.path.exists('SMSSpamCollection'):
        print("🇬🇧 Cargando base de datos en Inglés...")
        df_en = pd.read_csv('SMSSpamCollection', sep='\t', names=['label', 'message'])
        frames.append(df_en)
    
    # 2. Cargar Español
    if os.path.exists('spam_spanish.csv'):
        print("🇪🇸 Cargando refuerzo en Español...")
        df_es = pd.read_csv('spam_spanish.csv')
        frames.append(df_es)
        
    if not frames:
        raise FileNotFoundError("❌ No hay datos. Ejecuta primero 'generar_espanol.py'")
        
    df_final = pd.concat(frames, ignore_index=True)
    df_final['label_num'] = df_final.label.map({'ham': 0, 'spam': 1})
    
    print(f"📚 Total de mensajes para aprender: {len(df_final)}")
    return df_final

def train_model():
    """Entrena el modelo desde cero."""
    df = load_data_bilingue()
    
    X_train, X_test, y_train, y_test = train_test_split(
        df['message'], df['label_num'], test_size=0.2, random_state=42
    )
    
    vectorizer = CountVectorizer(strip_accents='unicode')
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    print("🧠 Entrenando IA Bilingüe (esto puede tardar un poco)...")
    model = MultinomialNB()
    model.fit(X_train_vec, y_train)
    
    acc = accuracy_score(y_test, model.predict(X_test_vec))
    print(f"🎯 Precisión del sistema: {acc * 100:.2f}%")
    
    return vectorizer, model

def predict(vectorizer, model, text):
    """Usa el modelo para predecir."""
    vec = vectorizer.transform([text])
    pred = model.predict(vec)
    prob = model.predict_proba(vec)[0]
    
    if pred[0] == 1:
        return f"🚨 SPAM (Seguridad: {prob[1]*100:.1f}%)"
    else:
        return f"✅ LEGÍTIMO (Seguridad: {prob[0]*100:.1f}%)"

if __name__ == "__main__":
    print("\n--- SISTEMA DE DETECCIÓN DE SPAM ---")

    # LÓGICA DE CARGA INTELIGENTE
    # 1. ¿Existen ya los archivos guardados?
    if os.path.exists(MODEL_FILE) and os.path.exists(VECTORIZER_FILE):
        print("💾 Cargando cerebro guardado...")
        try:
            model = joblib.load(MODEL_FILE)
            cv = joblib.load(VECTORIZER_FILE)
            print("✅ ¡Listo! Modelo cargado instantáneamente.")
        except:
            print("⚠️ Error cargando. Vamos a re-entrenar.")
            cv, model = train_model()
    else:
        # 2. Si no existen, entrenamos y guardamos
        print("⚠️ No hay memoria guardada. Iniciando entrenamiento...")
        cv, model = train_model()
        
        # Guardamos para la próxima vez
        joblib.dump(model, MODEL_FILE)
        joblib.dump(cv, VECTORIZER_FILE)
        print("💾 Modelo guardado en disco para el futuro.")
    
    # Bucle de prueba
    print("\n--- Escribe un mensaje para analizar (ES/EN) ---")
    while True:
        txt = input("\nMensaje (q para salir): ")
        if txt.lower() == 'q': break
        print(predict(cv, model, txt))