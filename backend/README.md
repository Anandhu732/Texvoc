# TxVoc Backend API

A powerful, modular FastAPI backend for the TxVoc text-to-speech application with voice cloning capabilities.

## 🎯 Overview

TxVoc Backend provides a comprehensive REST API for managing voice samples and generating speech synthesis. Built with FastAPI, it offers high performance, automatic API documentation, and seamless integration with the Next.js frontend.

## ✨ Features

- 🎤 **Voice Management**: Upload, store, and manage custom voice samples
- 🔊 **Speech Synthesis**: Convert text to speech using uploaded voices
- 📱 **Frontend Integration**: Seamless integration with Next.js frontend
- 📝 **Interactive Documentation**: Auto-generated API docs with Swagger UI
- 🔧 **Modular Design**: Clean, maintainable code structure
- 🚀 **Easy Setup**: One-command installation and setup
- 🔒 **Secure**: Input validation, CORS protection, and error handling
- 📊 **Monitoring**: Health checks and comprehensive logging

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment support

### Installation

1. **Run the setup script**:

   ```bash
   .\setup.bat
   ```

2. **Start the server**:

   ```bash
   # Activate virtual environment (if not already active)
   .venv\Scripts\activate

   # Start the API server
   python main.py
   ```

3. **Access the API**:
   - **API Base URL**: http://localhost:8000
   - **Interactive Documentation**: http://localhost:8000/docs
   - **Alternative Docs**: http://localhost:8000/redoc
   - **Health Check**: http://localhost:8000/health

## 📚 API Reference

### Core Endpoints

| Method | Endpoint  | Description                |
| ------ | --------- | -------------------------- |
| `GET`  | `/`       | API information and status |
| `GET`  | `/health` | Health check and metrics   |

### Voice Management

| Method   | Endpoint             | Description                |
| -------- | -------------------- | -------------------------- |
| `GET`    | `/voices`            | List all available voices  |
| `GET`    | `/voices/{voice_id}` | Get specific voice details |
| `POST`   | `/voices`            | Upload a new voice sample  |
| `DELETE` | `/voices/{voice_id}` | Delete a voice             |

### Speech Synthesis

| Method | Endpoint                    | Description               |
| ------ | --------------------------- | ------------------------- |
| `POST` | `/synthesize`               | Generate speech from text |
| `GET`  | `/synthesis/{synthesis_id}` | Get synthesis job details |
| `GET`  | `/synthesis`                | List all synthesis jobs   |

### Audio Files

| Method | Endpoint            | Description                    |
| ------ | ------------------- | ------------------------------ |
| `GET`  | `/audio/{filename}` | Download generated audio files |

## 💡 Usage Examples

### Upload a Voice Sample

```bash
curl -X POST "http://localhost:8000/voices" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@voice_sample.wav" \
  -F "name=My Custom Voice" \
  -F "description=A clear, professional voice" \
  -F "language=en"
```

**Response:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "My Custom Voice",
  "description": "A clear, professional voice",
  "language": "en",
  "created_at": "2025-08-29T00:00:00Z",
  "file_path": "/storage/voices/550e8400-e29b-41d4-a716-446655440000.wav",
  "duration": 10.5,
  "sample_rate": 22050
}
```

### Synthesize Speech

```bash
curl -X POST "http://localhost:8000/synthesize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a test of the TxVoc speech synthesis system.",
    "voice_id": "550e8400-e29b-41d4-a716-446655440000",
    "speed": 1.0,
    "pitch": 1.0
  }'
```

**Response:**

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "audio_url": "/audio/synthesis_123e4567-e89b-12d3-a456-426614174000.wav",
  "duration": 5.2,
  "voice_id": "550e8400-e29b-41d4-a716-446655440000",
  "text": "Hello, this is a test of the TxVoc speech synthesis system.",
  "created_at": "2025-08-29T00:00:00Z"
}
```

### List All Voices

```bash
curl -X GET "http://localhost:8000/voices"
```

### Health Check

```bash
curl -X GET "http://localhost:8000/health"
```

## 🏗️ Project Structure

```
backend/
├── main.py                 # Main FastAPI application
├── requirements.txt        # Python dependencies
├── setup.bat              # Setup script for Windows
├── start.bat              # Development server startup
├── README.md              # This documentation
├── .gitignore             # Git ignore rules
└── storage/               # File storage (created during setup)
    ├── voices/            # Uploaded voice samples
    │   └── .gitkeep       # Git tracking
    ├── audio/             # Generated audio files
    │   └── .gitkeep       # Git tracking
    └── temp/              # Temporary files
        └── .gitkeep       # Git tracking
```

## 🌐 Frontend Integration

This backend is designed to work seamlessly with the TxVoc Next.js frontend. The CORS configuration allows requests from:

- `http://localhost:3000` (default Next.js dev server)
- `http://127.0.0.1:3000`
- `http://localhost:3001` (alternative port)

### Frontend Usage Example

```javascript
// Upload a voice file
const uploadVoice = async (file, name, description) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("name", name);
  formData.append("description", description);

  const response = await fetch("http://localhost:8000/voices", {
    method: "POST",
    body: formData,
  });

  return await response.json();
};

// Synthesize speech
const synthesizeSpeech = async (text, voiceId) => {
  const response = await fetch("http://localhost:8000/synthesize", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text,
      voice_id: voiceId,
      speed: 1.0,
      pitch: 1.0,
    }),
  });

  return await response.json();
};
```

## 🔧 Configuration

### Environment Variables

The application uses sensible defaults but can be configured with environment variables:

```bash
HOST=0.0.0.0          # Server host
PORT=8000             # Server port
LOG_LEVEL=info        # Logging level (debug, info, warning, error)
CORS_ORIGINS=*        # Allowed CORS origins
```

### Supported Audio Formats

**Input (Voice Samples)**:

- WAV (.wav) - Recommended
- MP3 (.mp3)
- OGG (.ogg)
- FLAC (.flac)

**Output (Generated Speech)**:

- Currently generates placeholder files
- Ready for integration with TTS engines

## 🛠️ Development

### Running in Development Mode

```bash
# Activate virtual environment
.venv\Scripts\activate

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Start with auto-reload
python main.py
```

### Testing the API

1. **Interactive Documentation**: Visit http://localhost:8000/docs
2. **Health Check**: `curl http://localhost:8000/health`
3. **API Status**: `curl http://localhost:8000/`

### Code Structure

The application follows a modular structure:

- **Data Models**: Pydantic models for request/response validation
- **API Endpoints**: Organized by functionality (voices, synthesis, audio)
- **Utility Functions**: Helper functions for file handling and validation
- **Error Handling**: Centralized exception handling
- **Logging**: Structured logging throughout the application

## 🔌 Extending with TTS Engines

The backend is designed to be easily extended with actual TTS engines. The main synthesis function `generate_synthesis_audio()` in `main.py` currently creates placeholder files but can be replaced with:

### Coqui TTS Integration

```python
from TTS.api import TTS

def generate_synthesis_audio(text, voice_id, speed, pitch):
    # Initialize TTS
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

    # Generate audio
    voice_file = get_voice_file(voice_id)
    output_file = AUDIO_DIR / f"synthesis_{uuid.uuid4()}.wav"

    tts.tts_to_file(
        text=text,
        speaker_wav=voice_file,
        file_path=str(output_file),
        speed=speed
    )

    return output_file
```

### Other TTS Options

- **Google Text-to-Speech**: Cloud-based TTS service
- **Azure Speech Services**: Microsoft's TTS platform
- **AWS Polly**: Amazon's neural TTS
- **Tacotron 2**: Open-source neural TTS
- **WaveNet**: Google's neural audio generation

## 📊 Monitoring and Logging

### Health Monitoring

The `/health` endpoint provides:

- Server status
- Voice count
- Synthesis job count
- Timestamp information

### Logging

Structured logging includes:

- Request/response tracking
- Error monitoring
- Performance metrics
- Debug information

Logs are formatted with timestamps and severity levels for easy monitoring.

## 🔒 Security Features

- **CORS Protection**: Configured for specific frontend origins
- **File Type Validation**: Only allows specific audio formats
- **Request Size Limits**: Prevents oversized uploads
- **Input Sanitization**: Validates all user inputs
- **Error Message Sanitization**: Prevents information leakage

## 🚀 Production Deployment

For production deployment, consider:

### Server Configuration

```bash
# Use Gunicorn for production
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### Production Checklist

- [ ] Use a production WSGI server (Gunicorn, uWSGI)
- [ ] Set up a reverse proxy (Nginx, Apache)
- [ ] Configure SSL/TLS certificates
- [ ] Set up proper logging and monitoring
- [ ] Use a real database (PostgreSQL, MongoDB)
- [ ] Implement authentication if needed
- [ ] Set up backup strategies
- [ ] Configure environment variables
- [ ] Set up health monitoring
- [ ] Implement rate limiting

## 🧪 Testing

### Manual Testing

1. Start the server: `python main.py`
2. Visit the interactive docs: http://localhost:8000/docs
3. Test each endpoint using the Swagger UI

### Automated Testing

```bash
# Install testing dependencies
pip install pytest httpx

# Run tests (when test files are created)
pytest
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Submit a pull request

## 📝 API Documentation

### Data Models

#### Voice Model

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "language": "string",
  "created_at": "string",
  "file_path": "string",
  "duration": "number",
  "sample_rate": "number"
}
```

#### Synthesis Request

```json
{
  "text": "string",
  "voice_id": "string",
  "speed": "number (0.5-2.0)",
  "pitch": "number (0.5-2.0)"
}
```

#### Synthesis Response

```json
{
  "id": "string",
  "audio_url": "string",
  "duration": "number",
  "voice_id": "string",
  "text": "string",
  "created_at": "string"
}
```

## 🔗 Related Projects

- **TxVoc Frontend**: Next.js frontend application
- **TxVoc Mobile**: React Native mobile app (future)
- **TxVoc CLI**: Command-line interface (future)

## 📄 License

This project is part of the TxVoc application suite.

## 🆘 Support

For support and questions:

1. Check the [API Documentation](http://localhost:8000/docs)
2. Review this README
3. Check the logs for error messages
4. Open an issue in the repository

---

**Built with ❤️ using FastAPI and Python**
