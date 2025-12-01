<div align="center">

  <h1>🛡️ AI Spam Hunter</h1>

  <p>
    <strong>Detector de Spam Híbrido (Inglés/Español) con Interfaz Web Moderna</strong>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
    <img src="https://img.shields.io/badge/Scikit_Learn-Machine_Learning-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Sklearn" />
    <img src="https://img.shields.io/badge/HTML5-Frontend-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5" />
    <img src="https://img.shields.io/badge/Status-Activo-22c55e?style=for-the-badge" alt="Status" />
  </p>

  <p>
    <a href="#-demo">Ver Demo</a> •
    <a href="#-instalación">Instalación</a> •
    <a href="#-cómo-funciona">Arquitectura</a>
  </p>

</div>

---

## 📸 Demo

> *Interfaz gráfica moderna con Glassmorphism que conecta en tiempo real con una API de Inteligencia Artificial.*

---

## 🚀 Características

Este proyecto no es un simple script. Es una solución **Full Stack** de detección de amenazas.

* **🧠 IA Bilingüe:** Entrenado con el dataset *UCI SMS Collection* (Inglés) y reforzado con datos sintéticos en Español (Data Augmentation).
* **🔌 API REST:** Backend construido con **Flask** que sirve el modelo de Machine Learning (`naive_bayes`) como un microservicio.
* **🎨 UI Moderna:** Frontend en HTML5/CSS3/JS puro, sin frameworks pesados, con diseño responsivo y animaciones.
* **💾 Persistencia:** Sistema inteligente que guarda el modelo (`.pkl`) para evitar re-entrenamientos innecesarios.

---

## 🛠️ Tech Stack

| Componente | Tecnología | Descripción |
| :--- | :--- | :--- |
| **Modelo IA** | `Scikit-learn` | Algoritmo Multinomial Naive Bayes & CountVectorizer. |
| **Backend** | `Flask` | Servidor API REST que procesa las peticiones JSON. |
| **Persistencia** | `Joblib` | Serialización del modelo para cargas instantáneas. |
| **Frontend** | `HTML/JS/CSS` | Interfaz de usuario asíncrona (`fetch` API). |

---

## 📦 Instalación

Sigue estos pasos para desplegar el proyecto en tu máquina local:

1.  **Clonar el repositorio**
    ```bash
    git clone [https://github.com/TU-USUARIO/ai-spam-hunter.git](https://github.com/TU-USUARIO/ai-spam-hunter.git)
    cd ai-spam-hunter
    ```

2.  **Instalar dependencias**
    ```bash
    python -m pip install -r requirements.txt
    ```
    *(Asegúrate de tener `flask`, `flask-cors`, `pandas`, `scikit-learn`, `joblib`)*

---

## ⚡ Guía de Inicio Rápido

Para ejecutar la aplicación necesitas dos terminales (Arquitectura Cliente-Servidor):

### Paso 1: Encender el Cerebro (Backend)
Abre una terminal y ejecuta:
```bash
python api.py
Verás: Running on http://127.0.0.1:5000

Paso 2: Abrir la Web (Frontend)
Ve a la carpeta del proyecto y haz doble clic en el archivo: index.html

¡Listo! Escribe un mensaje y observa cómo la IA lo clasifica en tiempo real.

📂 Estructura del Proyecto

📁 ai-spam-hunter
├── 📄 api.py              # Servidor Flask (Backend)
├── 📄 spam_detector.py    # Script de entrenamiento (Fábrica de modelos)
├── 📄 index.html          # Interfaz de Usuario (Frontend)
├── 🧠 spam_model.pkl      # Modelo entrenado (Generado auto.)
├── 🧠 vectorizer.pkl      # Vocabulario (Generado auto.)
├── 📊 SMSSpamCollection   # Dataset original
└── 📄 README.md           # Documentación

<div align="center"> <p> Hecho con ❤️ y mucha ☕ usando Python. </p> </div>

-----

### ¿Cómo hacer que quede perfecto? (El toque final)

Para que el README luzca como el de una empresa de Silicon Valley, haz esto:

1.  **Haz una captura de pantalla:** Abre tu web (`index.html`), escribe un mensaje de prueba para que se vea el resultado (rojo o verde) y haz una captura de pantalla bonita.
2.  **Guárdala:** Ponle el nombre `screenshot.png` y métela en la misma carpeta del proyecto.
3.  **Sube todo a GitHub:**
    ```bash
    git add .
    git commit -m "Mejorando docs"
    git push
    ```
4.  **Descomenta la línea de la imagen:** En el código que te di arriba, busca donde dice `y quítale las flechitas` para que se vea así: `![Captura de la App](screenshot.png)`.

¡Cuando entres a tu repo verás los escudos de colores, las tablas organizadas y la imagen de tu proyecto\!
