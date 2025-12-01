import pandas as pd
from deep_translator import GoogleTranslator
import time
import os

# --- CONFIGURACIÓN ---
SOURCE_FILE = 'SMSSpamCollection'
OUTPUT_FILE = 'spam_spanish.csv'
CANTIDAD_A_TRADUCIR = 300  # Traducirá 150 spam y 150 ham

def generar_datos_espanol():
    if not os.path.exists(SOURCE_FILE):
        print(f"❌ Error: No encuentro '{SOURCE_FILE}'.")
        return

    print("--- 1. LEYENDO DATOS ORIGINALES ---")
    df = pd.read_csv(SOURCE_FILE, sep='\t', names=['label', 'message'])

    # Cogemos una muestra equilibrada para traducir
    df_spam = df[df['label'] == 'spam'].head(int(CANTIDAD_A_TRADUCIR/2))
    df_ham = df[df['label'] == 'ham'].head(int(CANTIDAD_A_TRADUCIR/2))
    subset = pd.concat([df_spam, df_ham])

    print(f"--- 2. TRADUCIENDO {len(subset)} MENSAJES AL ESPAÑOL ---")
    print("Esto puede tardar unos 2-3 minutos. Paciencia...")

    translator = GoogleTranslator(source='en', target='es')
    nuevos_datos = []
    contador = 0

    for index, row in subset.iterrows():
        try:
            # Traducimos
            texto_es = translator.translate(row['message'])
            nuevos_datos.append([row['label'], texto_es])
            
            contador += 1
            if contador % 10 == 0:
                print(f"   ✅ {contador} mensajes listos...")
            
            # Pausa técnica para evitar bloqueos
            time.sleep(0.1)
            
        except Exception as e:
            print(f"   ⚠️ Fallo en uno: {e}")

    # Guardamos
    df_es = pd.DataFrame(nuevos_datos, columns=['label', 'message'])
    df_es.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print(f"\n🎉 ¡LISTO! Archivo '{OUTPUT_FILE}' creado.")

if __name__ == "__main__":
    generar_datos_espanol()