# 🎨 Narrated Art Experience

### Transform stories into AI-generated art with voice narration.

An AI-powered web application that combines **AI storytelling, dynamic image generation, and text-to-speech** to create an immersive art experience. Built with Flask and powered by Google Gemini, Pollinations AI, and gTTS — with Docker for easy deployment.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **AI Storytelling** | Generates immersive narratives using the Google Gemini API. |
| 🖼️ **AI Image Generation** | Creates visual artwork inspired by the generated story using Pollinations AI. |
| 🔊 **Voice Narration** | Converts generated narratives into audio using Google Text-to-Speech (gTTS). |
| 🌐 **Web Application** | Provides a Flask-based interface to bring the experience together. |
| 🐳 **Docker Support** | Containerized for consistent setup and deployment. |

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![gTTS](https://img.shields.io/badge/Text--to--Speech-FF9800?style=for-the-badge)
![AI Image Generation](https://img.shields.io/badge/AI%20Image%20Generation-9B59B6?style=for-the-badge)

---

## ⚙️ Prerequisites

Before getting started, make sure you have:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- A [Google Gemini API key](https://aistudio.google.com/apikey).
- Git installed on your system.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/mallesh-bhandari/narrated-art-experience.git
cd narrated-art-experience
```

### 2. Configure Environment Variables

Create a `.env` file in the project root and add your Gemini API key using the environment variable name expected by your application.

```env
GEMINI_API_KEY=your_api_key_here
```

> **Note:** Make sure the variable name matches the one used in your Python code. Never commit your real API key to GitHub.

### 3. Build the Docker Image

```bash
docker build -t narrated-art-experience .
```

### 4. Run the Application

Use the port configured in your Dockerfile or application. For example, if the container listens on port `5000`:

```bash
docker run --env-file .env -p 5000:5000 narrated-art-experience
```

Open your browser and visit:

```text
http://localhost:5000
```

> **Tip:** If your project already uses Docker Compose, you can use `docker compose up --build` instead, provided the Compose configuration is set up correctly.

---

## 🔄 How It Works

1. **Enter a prompt** — Start with an idea or story concept.
2. **Generate a narrative** — Google Gemini creates an engaging description.
3. **Create artwork** — Pollinations AI generates an image based on the narrative.
4. **Listen to the story** — gTTS converts the generated text into spoken audio.
5. **Experience the result** — Explore the combination of storytelling, visuals, and narration through the web application.

---

## 📂 Project Structure

```text
narrated-art-experience/
├── app.py                 # Flask application (example filename)
├── templates/             # HTML templates
├── static/                # CSS, JavaScript, and generated assets
├── Dockerfile             # Docker build configuration
├── requirements.txt       # Python dependencies
├── .env                   # Local environment variables (not committed)
├── .gitignore             # Files excluded from Git
└── README.md              # Project documentation
```

*Adjust the filenames and folders above to match your actual repository.*

---

## 🔐 Security

- Store API keys in environment variables.
- Keep `.env` out of version control.
- Never expose API credentials in source code or public repositories.

---

## 👨‍💻 Author

**Mallesh Bhandari**

[![GitHub](https://img.shields.io/badge/GitHub-mallesh--bhandari-181717?style=for-the-badge&logo=github)](https://github.com/mallesh-bhandari)

---

## 📄 License

Add your preferred open-source license here, such as the MIT License, if applicable.

---

<p align="center">
  <b>✨ Turning imagination into stories, art, and sound. ✨</b>
</p>
