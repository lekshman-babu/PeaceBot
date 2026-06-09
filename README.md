# 🕊️ **PeaceBot – Mental Health Chatbot Application**

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![TensorFlow](https://img.shields.io/badge/ML-TensorFlow-orange?logo=tensorflow)
![Keras](https://img.shields.io/badge/Deep%20Learning-Keras-red?logo=keras)
![Flask](https://img.shields.io/badge/Backend-Flask-black?logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite)
![Jupyter](https://img.shields.io/badge/Notebook-Jupyter-orange?logo=jupyter)
![Status](https://img.shields.io/badge/Status-Prototype-yellow)

---

## ✨ Overview

**PeaceBot** is a mental health chatbot application built using Python, Flask, SQLite, TensorFlow, and Keras.

The project combines a web-based chat interface with a custom Transformer-based chatbot model. Users can sign up, log in, send messages, and receive chatbot responses through a Flask application. Chat history is stored in a local SQLite database.

---

## 🎯 Problem Statement

Many people need a simple, accessible space to express their thoughts and receive supportive responses.  
Traditional mental health support tools can be difficult to access, while basic chatbots often lack personalized conversation flow.

**PeaceBot** aims to provide a prototype chatbot system that can:

- Accept user messages through a web interface
- Generate chatbot replies using a trained deep learning model
- Store user login details
- Save previous chat conversations
- Demonstrate an end-to-end mental health chatbot workflow

---

## 💡 Solution: PeaceBot

| Feature | Description |
|---------|-------------|
| 💬 **Chatbot Interface** | Provides a web-based chat page where users can interact with the bot. |
| 🔐 **User Login & Signup** | Supports user authentication using SQLite-backed login storage. |
| 🧠 **Transformer Model** | Uses a custom encoder-decoder Transformer architecture for response generation. |
| 🗄️ **Chat History Storage** | Stores conversation history for each user in a local SQLite database. |
| 📚 **Dataset-Based Responses** | Uses chatbot datasets to improve response matching and fallback replies. |
| 🌐 **Flask Backend** | Serves the login, signup, and chat routes for the application. |

---

## 🧰 Tech Stack

| Layer | Technologies |
|-------|--------------|
| **Language** | Python |
| **Backend** | Flask, Flask-SocketIO |
| **Machine Learning** | TensorFlow, Keras |
| **Model Architecture** | Transformer, Encoder, Decoder, Multi-Head Self-Attention |
| **Database** | SQLite |
| **Data Processing** | Pandas, NumPy |
| **Frontend** | HTML, CSS, JavaScript |
| **Notebook** | Jupyter Notebook |

---

## 🏗️ Project Architecture

```text
User
 ↓
Flask Web App
 ↓
Login / Signup / Chat Routes
 ↓
SQLite Database
 ↓
Inference Pipeline
 ↓
Transformer Chatbot Model
 ↓
Generated Bot Response
 ↓
Chat History Storage
```

---

## 📁 Project Structure

```text
PeaceBot/
├── README.md
├── Chatbot.ipynb
└── Application/
    ├── FlaskEnd.py
    ├── Inference.py
    ├── Transformer.py
    ├── Encoder.py
    ├── Decoder.py
    ├── MultiHeadSelfAttention.py
    ├── DatasetAccess.py
    ├── HyperParametersLoader.py
    ├── LoginDatabaseAccess.py
    ├── ChatDatabaseAccess.py
    ├── Database/
    ├── Parameters/
    ├── static/
    └── templates/
```

---

## ⚙️ Setup Guide

### 1️⃣ Clone Repository

```bash
git clone https://github.com/lekshman-babu/PeaceBot.git
cd PeaceBot
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

For Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install flask flask-socketio tensorflow keras pandas numpy
```

### 4️⃣ Run the Application

```bash
python Application/FlaskEnd.py
```

Then open the local Flask URL in your browser.

---

## 🧠 Model Details

PeaceBot uses a custom Transformer-based chatbot model with:

- Encoder blocks
- Decoder blocks
- Multi-head self-attention
- Positional embeddings
- Feed-forward layers
- Dropout regularization
- Tokenized question and reply sequences

The model loads saved architecture, tokenizers, hyperparameters, and trained weights during inference.

---

## 🔑 Core Components

| File | Purpose |
|------|---------|
| `FlaskEnd.py` | Main Flask application with login, signup, and chat routes. |
| `Inference.py` | Loads the chatbot model and generates responses. |
| `Transformer.py` | Defines the full Transformer model. |
| `Encoder.py` | Implements Transformer encoder blocks. |
| `Decoder.py` | Implements Transformer decoder blocks. |
| `MultiHeadSelfAttention.py` | Implements attention and feed-forward layers. |
| `DatasetAccess.py` | Loads chatbot datasets for response matching. |
| `HyperParametersLoader.py` | Loads hyperparameters and tokenizer files. |
| `LoginDatabaseAccess.py` | Handles login database operations. |
| `ChatDatabaseAccess.py` | Handles chat history database operations. |
| `Chatbot.ipynb` | Notebook used for chatbot experimentation and model development. |

---

## 📌 Features

- User signup and login
- Web-based chatbot interface
- Transformer-based response generation
- SQLite-backed user storage
- SQLite-backed chat history storage
- Dataset-based fallback responses
- Modular deep learning architecture
- Jupyter notebook for experimentation

---

## 🚀 Use Cases

- Mental health chatbot prototype
- Conversational AI experimentation
- Transformer model learning project
- Flask chatbot application
- SQLite-based chat storage system
- End-to-end deep learning chatbot demo

---

## 🔮 Future Improvements

- Add stronger authentication and password hashing
- Improve UI/UX for the chat interface
- Add crisis-support disclaimers and emergency resource guidance
- Improve response safety and moderation
- Add model evaluation metrics
- Add `requirements.txt`
- Add deployment instructions
- Add REST API documentation
- Store conversations in a safer structured format instead of raw string evaluation
- Improve dataset quality and response filtering

---

## ⚠️ Disclaimer

PeaceBot is a prototype chatbot project and should **not** be used as a replacement for professional mental health support.

If someone is in immediate danger or experiencing a crisis, they should contact local emergency services or a qualified mental health professional.

---

## 🧑‍💻 Author

**Lekshman Babu**

---

## 🪪 License

No license file is currently included. Add a license before using or distributing the project publicly.

---

> 🕊️ *PeaceBot is a prototype mental health chatbot that combines Flask, SQLite, and a custom Transformer model to provide supportive conversational responses.*
