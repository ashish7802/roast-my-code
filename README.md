diff --git a/README.md b/README.md
index d7bd89a4a421bfb65ae29688cbd96f4f99906993..372f7dd5fc01fe8ec3c9fa8ec4df81b64b89b64b 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,80 @@
-# roast-my-code
\ No newline at end of file
+# Roast My Code (Full-Stack)
+
+A full-stack version of **Roast My Code** with:
+- **Backend:** FastAPI + SQLite + JWT auth
+- **Frontend:** Single-file HTML/CSS/Vanilla JS
+- **AI Roast Engine:** Anthropic Claude Sonnet 4
+
+## Project Structure
+
+```text
+roast-my-code/
+├── backend/
+│   ├── main.py
+│   ├── auth.py
+│   ├── database.py
+│   ├── models.py
+│   ├── requirements.txt
+│   └── .env.example
+├── frontend/
+│   └── index.html
+└── README.md
+```
+
+## 1) Backend Setup
+
+```bash
+cd backend
+python3 -m venv .venv
+source .venv/bin/activate
+pip install -r requirements.txt
+```
+
+Create your `.env` file:
+
+```bash
+cp .env.example .env
+```
+
+Edit `.env` and set real values:
+
+```env
+ANTHROPIC_API_KEY=your_real_anthropic_key
+JWT_SECRET=your_long_random_secret
+```
+
+Run the FastAPI server:
+
+```bash
+uvicorn main:app --reload
+```
+
+Backend will run at `http://localhost:8000`.
+
+## 2) Frontend Setup
+
+Open `frontend/index.html` with a local static server (recommended):
+
+```bash
+cd frontend
+python3 -m http.server 5500
+```
+
+Then open:
+- `http://localhost:5500/index.html`
+
+## 3) How It Works
+
+- Open the frontend page.
+- Register a user account (first time).
+- Log in to receive a JWT token (stored in `localStorage`).
+- Paste code, select intensity, click **Roast It!**.
+- Frontend calls `POST http://localhost:8000/roast` with `Authorization: Bearer <token>`.
+- If token is missing/expired, user is returned to login.
+
+## API Endpoints
+
+- `POST /auth/register` → body `{ "username": "...", "password": "..." }`
+- `POST /auth/login` → body `{ "username": "...", "password": "..." }` returns JWT token
+- `POST /roast` → body `{ "code": "...", "intensity": "Gentle|Medium|Savage" }` (requires bearer token)
+- `GET /health` → health check
