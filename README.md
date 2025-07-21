# Reasoning Chatbot (ChatGPT-4o Mini)

A minimal, modular, web-based reasoning chatbot using OpenAI ChatGPT-4o Mini. Designed for fast, stateless, context-driven reasoning with daily context switching.

---

## Features
- FastAPI backend (Python)
- ChatGPT-4o Mini API integration (text-only, API key hardcoded)
- Daily context via `context.yaml` (admin-editable)
- Minimal, embeddable frontend chat widget (HTML/JS/CSS)
- Stateless: no user data stored
- Modular LLM adapter (swap OpenAI for others easily)
- REST and streaming endpoints

---

## 📦 Setup & Local Run

### 1. Clone & Install Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Edit Daily Context
Edit `backend/context.yaml` to set the topic and constraints for the day.

### 3. Run Backend
```bash
uvicorn main:app --reload
```

### 4. Serve Frontend
You can open `frontend/index.html` directly, or serve it with any static server:
```bash
cd ../frontend
python3 -m http.server 8080
# Then open http://localhost:8080 in your browser
```

---

## 🛠️ Deployment

### Docker (Optional)
A sample Dockerfile is provided in `backend/`.
```bash
cd backend
sudo docker build -t reasoning-chatbot .
sudo docker run -p 8000:8000 reasoning-chatbot
```

### Public Hosting
- Deploy backend to Fly.io, Railway, or any VPS
- Serve frontend from any static host (Netlify, Vercel, S3, etc.)
- Use a public tunnel (e.g. ngrok) for local testing:
  ```bash
  ngrok http 8000
  ```

---

## 🧪 Testing
- Use `curl` or Postman to POST to `/chat` endpoint:
  ```bash
  curl -X POST http://localhost:8000/chat -H 'Content-Type: application/json' -d '{"user_input": "How do I solve a problem?"}'
  ```
- Or use the chat widget in your browser.

---

## 📝 Modularity
- To swap LLMs, edit or add a new adapter in `backend/llm/` and update usage in `main.py`.
- To change context, just edit `context.yaml` and restart the backend.

---

## 📁 File Structure
```
backend/
  main.py           # FastAPI app
  config.py         # Context loader
  llm/
    base.py        # LLM interface
    openai.py      # OpenAI adapter (ChatGPT-4o Mini)
  schemas.py        # API models
  context.yaml      # Daily context
  requirements.txt
  Dockerfile        # (optional)
frontend/
  index.html        # Chat widget demo
  chat.js           # Widget logic
  style.css         # Widget styles
README.md
```

---

## ❓ FAQ
- **How do I change the chatbot's behavior?**
  - Edit `backend/context.yaml` and restart the backend.
- **How do I embed the chat widget?**
  - Copy `chat.js` and `style.css` into your site, and use the HTML from `index.html`.
- **How do I use a different LLM?**
  - Implement a new adapter in `backend/llm/` and update `main.py`.

---

MIT License