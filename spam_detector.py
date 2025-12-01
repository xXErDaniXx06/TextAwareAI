import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

def load_data():
    """
    Loads the SMS Spam Collection dataset from a file.
    """
    filename = 'SMSSpamCollection'
    
    if not os.path.exists(filename):
        raise FileNotFoundError(f"❌ Error: No encontré el archivo '{filename}'. Asegúrate de descargarlo y ponerlo en esta carpeta.")

    print(f"Loading data from {filename}...")
    
    # El archivo está separado por tabulaciones (\t), no por comas
    df = pd.read_csv(filename, sep='\t', names=['label', 'message'])
    
    # Convertimos etiquetas a números: 'spam' -> 1, 'ham' -> 0
    df['label_num'] = df.label.map({'ham': 0, 'spam': 1})
    
    print(f"Data loaded! Total messages: {len(df)}")
    print(f"Spam messages: {len(df[df['label']=='spam'])}")
    print(f"Ham messages: {len(df[df['label']=='ham'])}")
    
    return df

def train_model():
    """
    Trains the model with real data.
    """
    # 1. Load Data
    try:
        df = load_data()
    except Exception as e:
        print(e)
        return None, None

    # 2. Split Data
    X_train, X_test, y_train, y_test = train_test_split(
        df['message'], df['label_num'], test_size=0.25, random_state=42
    )
    
    # 3. Vectorization
    vectorizer = CountVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # 4. Train Model
    print("Training model (this might take a second)...")
    model = MultinomialNB()
    model.fit(X_train_vec, y_train)
    
    # 5. Evaluate
    predictions = model.predict(X_test_vec)
    acc = accuracy_score(y_test, predictions)
    print(f"\nModel trained successfully!")
    print(f"Accuracy: {acc * 100:.2f}%")
    print("\nDetailed Report:\n")
    print(classification_report(y_test, predictions, target_names=['Ham', 'Spam']))
    
    return vectorizer, model

def predict_message(vectorizer, model, text):
    """
    Predicts if a specific message is Spam or Ham.
    """
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)
    return "🚨 SPAM" if prediction[0] == 1 else "✅ HAM (Safe)"

if __name__ == "__main__":
    print("--- REAL SPAM DETECTOR AI ---")
    
    cv, clf = train_model()
    
    if cv and clf:
        print("\n--- TEST AREA ---")
        print("Tip: Try English messages (e.g., 'Win a free prize now!' or 'Hey, are you home?')")
        while True:
            user_input = input("\nEnter message (or 'q' to quit): ")
            if user_input.lower() == 'q':
                break
            result = predict_message(cv, clf, user_input)
            print(f"Result: {result}")