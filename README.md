# 🔥 Roast My Code (Full-Stack)

> A full-stack app that lets Claude Sonnet 4 **brutally (or gently) roast your code** — with auth, history, and adjustable savage levels.

---

## 🧱 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + SQLite + JWT Auth |
| Frontend | Single-file HTML / CSS / Vanilla JS |
| AI Engine | Anthropic Claude Sonnet 4 |

---

## 📁 Project Structure

```text
roast-my-code/
├── backend/
│   ├── main.py              # FastAPI app + roast endpoint
│   ├── auth.py              # JWT login/register logic
│   ├── database.py          # SQLite setup
│   ├── models.py            # Pydantic models
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variable template
├── frontend/
│   └── index.html           # Full UI in one file
└── README.md
```

---

## ⚙️ Backend Setup

### 1. Create & activate virtual environment

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in real values:

```env
ANTHROPIC_API_KEY=your_real_anthropic_key
JWT_SECRET=your_long_random_secret_here
```

> ⚠️ Never commit your `.env` file. It's already in `.gitignore`.

### 4. Start the server

```bash
uvicorn main:app --reload
```

Backend runs at → `http://localhost:8000`

You can explore the auto-generated API docs at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 🖥️ Frontend Setup

Serve the frontend using Python's built-in HTTP server:

```bash
cd frontend
python3 -m http.server 5500
```

Then open in your browser:

```
http://localhost:5500/index.html
```

> ✅ Using a local server avoids CORS issues with `fetch()` calls to the backend.

---

## 🚀 How It Works

```
User visits frontend
       │
       ▼
Register / Login  ──► JWT token stored in localStorage
       │
       ▼
Paste code + select intensity (Gentle / Medium / Savage)
       │
       ▼
POST /roast  (Authorization: Bearer <token>)
       │
       ▼
FastAPI validates token → calls Claude Sonnet 4
       │
       ▼
Roast response displayed on screen 🔥
```

If the token is **missing or expired**, the user is automatically returned to the login screen.

---

## 📡 API Endpoints

### Auth

| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| `POST` | `/auth/register` | `{ "username": "...", "password": "..." }` | Create a new account |
| `POST` | `/auth/login` | `{ "username": "...", "password": "..." }` | Returns a JWT token |

### Roast

| Method | Endpoint | Body | Auth Required |
|--------|----------|------|---------------|
| `POST` | `/roast` | `{ "code": "...", "intensity": "Gentle\|Medium\|Savage" }` | ✅ Bearer token |

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Returns server status |

---

## 🔐 Authentication Flow

```
POST /auth/login
  → returns: { "access_token": "eyJ...", "token_type": "bearer" }

Store in localStorage:
  localStorage.setItem("token", access_token)

Use in requests:
  headers: { "Authorization": "Bearer <token>" }
```

---

## 🌶️ Roast Intensity Levels

| Level | What to Expect |
|-------|---------------|
| **Gentle** | Kind nudges, polite suggestions |
| **Medium** | Honest feedback with some sass |
| **Savage** | Zero mercy. Claude will not hold back. |

---

## 🛠️ Requirements

**Backend (`requirements.txt`):**

```
fastapi
uvicorn[standard]
python-jose[cryptography]
passlib[bcrypt]
anthropic
python-dotenv
```

**Frontend:** No build step. Pure HTML + CSS + Vanilla JS.

---

## 🔒 Security Notes

- Passwords are hashed with **bcrypt** via `passlib`
- JWTs are signed using the `JWT_SECRET` from `.env`
- Tokens expire after a configurable TTL (default: 60 minutes)
- Never expose your `ANTHROPIC_API_KEY` on the frontend

---

## 🧪 Quick Test (curl)

```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "ashish", "password": "test123"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "ashish", "password": "test123"}'

# Roast (replace TOKEN with the JWT from login)
curl -X POST http://localhost:8000/roast \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"code": "for i in range(len(arr)): print(arr[i])", "intensity": "Savage"}'
```

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m "Add my feature"`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

MIT License — feel free to use, modify, and deploy.

---

Built with ❤️ and a lot of Claude roasting sessions.
