# 🚀 MYTHIQ.AI — Ultimate Self-Learning AI Empire

Launch your own ChatGPT-style AI with persistent memory, branching logic, and multimodal capability in minutes. Built for creators, developers, and dreamers who want a smarter assistant that learns over time.

---

## ✨ Features

- 🧠 **Self-Learning AI** — Evolves with every conversation using branching modules
- 💬 **Natural Chat Interface** — Engages like ChatGPT, enhanced with memory and creativity
- 📚 **Persistent Memory** — Remembers user preferences and factual statements across sessions
- 🎨 **Creative Engine** — Assists with brainstorming, image generation, and lore synthesis
- 🔄 **Modular Dispatch System** — Dynamic routing and fallback-safe scoring
- 🌐 **Responsive Web UI** — Integrated front-end optimized for fast interaction
- 🚀 **Railway-Ready** — Quick to deploy on Railway with Docker support and Nixpacks

---

## 🛠️ Tech Stack

| Layer         | Tools & Frameworks                         |
|---------------|--------------------------------------------|
| Backend       | Flask, Gunicorn, SocketIO                  |
| AI Modules    | Transformers, SentenceTransformers, Torch |
| Memory Core   | SQLite or modular memory integration       |
| Frontend      | HTML/CSS/JavaScript (creator_ui)          |
| Diagnostics   | Self-learning, fallback scoring            |
| Deployment    | Railway, Docker, Gunicorn, Nixpacks        |

---

## 📦 Setup & Deployment

### 🔧 Local Development

```bash
# Install runtime dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Run the app
python main.py
