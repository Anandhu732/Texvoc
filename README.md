# TxVoc - Text-to-Speech with Voice Cloning

A modern text-to-speech application with custom voice cloning capabilities. Upload voice samples and generate speech synthesis using those custom voices.

![Next.js](https://img.shields.io/badge/Next.js-15.5.2-black?style=flat-square&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green?style=flat-square&logo=fastapi)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=flat-square&logo=typescript)

## ✨ Features

- 🎤 Upload custom voice samples (WAV, MP3, OGG, FLAC)
- 🔊 Convert text to speech using uploaded voices
- 🎨 Modern dark theme with responsive design
- ⚙️ Adjustable speech parameters (speed, pitch)
- 📱 Drag-and-drop file uploads

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+

### Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/Anandhu732/Textvoc.git
   cd Textvoc
   ```

2. **Backend setup**

   ```bash
   cd backend
   .\setup.bat          # Windows setup script
   python main.py       # Start API server
   ```

3. **Frontend setup** (in new terminal)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Access

- **Application**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

## �️ Tech Stack

**Frontend**: Next.js 15, TypeScript, TailwindCSS, shadcn/ui
**Backend**: FastAPI, Python, Pydantic
**Features**: File upload, audio processing, REST API

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

