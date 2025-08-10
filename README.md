# GenAI

**AI-Powered Video Editing & Content Generation Platform**

Built in **24 hours** during a hackathon, GenAI won **1st place**, a **₹30,000 prize**, and judges offered internships and explored launching their own AI startup with us.

---

## 🚀 Overview

GenAI is a modular toolset for content creators:

* **shortGen/** – Automatically extracts short highlights from long-form videos and uploads them to YouTube.
* **aivideogen/** – Generates AI-driven video snippets from text prompts, including audio, captions, and rendering.
* **aizoom/** – Applies intelligent zoom and autofocus effects to existing video content.
* **ui/** – A Next.js + Tailwind frontend that orchestrates these services with uploads, previews, and analytics.

---

## 📦 Architecture

```
           +-------------------+
           |   Client Browser  |
           +--------+----------+
                    |
                    v
              +-----+------+
              |   Next.js   |
              +-----+------+
                    |
        +-----------+------------+
        |           |            |
        v           v            v
+-------+------+ +-----------+ +------------+
| shortGen API | | aivideogen | | aizoom API |
+--------------+ +-----------+ +------------+
        |              |              |
        +--------------+--------------+
                       |
                 +-----+------+
                 | YouTube API|
                 +------------+
```

Each service runs independently and communicates via REST endpoints.

---

## 🛠️ Installation & Setup

1. **Install dependencies**

   ```bash
   pip install -r shortGen/requirements.txt
   pip install -r aivideogen/requirements.txt
   pip install -r aizoom/requirements.txt
   npm install --prefix ui
   ```

2. **Configure environment**

   * Copy `.env.example` in `aivideogen/` and fill in API keys.
   * Place `cred.json` (YouTube credentials) and `youtube_token.pickle` in `shortGen/`.

3. **Run each component** (in separate terminals):

   ```bash
   cd shortGen && venv/Scripts/activate python app.py
   cd ../aivideogen && venv/Scripts/activate python app.py
   cd ../aizoom && venv/Scripts/activate python app.py
   cd ../ui && npm run dev
   ```

Visit `http://localhost:3000` for the web UI.

---

## 💡 Usage Flow

1. Upload a long-form video or enter a text prompt via the UI.
2. `shortGen` extracts highlights and handles YouTube uploads.
3. `aivideogen` generates video from prompts.
4. `aizoom` adds dynamic zoom/autofocus effects.
5. Preview clips in the browser or publish directly to YouTube.

---

## 🚀 Highlights & Impact

* **Hackathon Winner** – Built in 24 hours, won first place and internships from judges.
* **AI-Driven Toolkit** – Combines text-to-video, highlight extraction, and smart editing.
* **Modular & Extensible** – Independent services simplify enhancements and scaling.

---

## 🤝 Contributing

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit changes and push
4. Open a Pull Request

---
