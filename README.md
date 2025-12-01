# 🛡️ AI Spam Hunter

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green?style=for-the-badge&logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

**AI Spam Hunter** is a high-performance machine learning application designed to detect spam messages with precision. It leverages **Multinomial Naive Bayes** and **Feature Engineering** to analyze text patterns and provide real-time classification.

## ✨ Features

*   **🚀 High Performance**: Uses Multinomial Naive Bayes for fast and effective text classification.
*   **🧠 Explainable AI (XAI)**: Highlights specific words that triggered the spam detection based on Bayesian probabilities.
*   **Feature Engineering**: Custom token injection for URLs, money symbols, and urgency indicators.
*   **🌍 Bilingual Support**: Trained on English and Spanish datasets.
*   **🎨 Modern UI**: Glassmorphism design with dark mode and smooth animations.
*   **🌐 Internationalization**: Toggle between English and Spanish interfaces instantly.
*   **⚡ Real-time Analysis**: Instant feedback with confidence scores.

## 🛠️ Tech Stack

*   **Backend**: Python, Flask, scikit-learn, pandas, joblib.
*   **Frontend**: HTML5, CSS3 (Glassmorphism), JavaScript (Vanilla).
*   **Model**: Multinomial Naive Bayes with CountVectorizer and custom feature engineering.

## 🚀 Getting Started

### Prerequisites

*   Python 3.8 or higher.
*   pip (Python package manager).

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/TextAwareAI.git
    cd TextAwareAI
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Train the model** (First time only):
    ```bash
    python spam_detector.py
    ```
    *This will generate `spam_model.pkl` and `vectorizer.pkl`.*

4.  **Run the API**:
    ```bash
    python api.py
    ```

5.  **Open the App**:
    Visit `http://127.0.0.1:5000` in your browser.

## 🔍 How it Works

1.  **Input**: The user enters a message.
2.  **Feature Engineering**: The system injects special tokens for URLs, money symbols, and urgency indicators.
3.  **Vectorization**: The text is converted into numerical vectors using TF-IDF.
4.  **Prediction**: The SVM model classifies the vector as Spam or Ham.
5.  **Explanation**: If Spam, the system analyzes the SVM coefficients to identify and highlight the most "spammy" words.

## 👤 Author

**Daniel Carrasco García**

*   **Rights**: All rights reserved © 2025.

---
*Disclaimer: This tool is for educational and guidance purposes only. Always verify the source of suspicious messages.*
