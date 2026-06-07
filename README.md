# AI Humanizer

A powerful API service that converts high-AIGC characteristic text into natural human-style writing.

## Features

- 🎯 Single text humanization
- 📦 Batch processing support
- 🎚️ Multiple intensity levels (Light, Medium, Strong, Custom)
- 🚀 Fast and lightweight (FastAPI)
- 💻 Local deployment ready
- 📝 RESTful API interface

## Installation

```bash
git clone https://github.com/mengfeizhanshen/ai-humanizer.git
cd ai-humanizer
pip install -r requirements.txt
```

## Quick Start

### Linux/Mac
```bash
bash run.sh
```

### Windows
```bash
run.bat
```

### Manual Start
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

### Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Single Text Humanization

**Endpoint:** `POST /humanize`

**Request:**
```json
{
  "text": "The integration of artificial intelligence technology has fundamentally transformed the landscape of modern society, thereby necessitating comprehensive adaptation strategies.",
  "intensity": "medium"
}
```

**Response:**
```json
{
  "original": "The integration of artificial intelligence technology has fundamentally transformed the landscape of modern society, thereby necessitating comprehensive adaptation strategies.",
  "humanized": "AI technology has changed how society works today, and we need to adapt to these changes.",
  "intensity": "medium",
  "score": 0.82
}
```

### Batch Processing

**Endpoint:** `POST /humanize-batch`

**Request:**
```json
{
  "texts": [
    "Text one to humanize...",
    "Text two to humanize..."
  ],
  "intensity": "strong"
}
```

**Response:**
```json
{
  "results": [
    {
      "original": "Text one to humanize...",
      "humanized": "Humanized version of text one...",
      "intensity": "strong",
      "score": 0.95
    },
    {
      "original": "Text two to humanize...",
      "humanized": "Humanized version of text two...",
      "intensity": "strong",
      "score": 0.93
    }
  ],
  "total": 2,
  "success_count": 2
}
```

### Get Intensity Levels

**Endpoint:** `GET /intensity-levels`

**Response:**
```json
{
  "available_levels": [
    {
      "name": "light",
      "description": "Minimal changes, preserves original meaning"
    },
    {
      "name": "medium",
      "description": "Balanced transformation"
    },
    {
      "name": "strong",
      "description": "Significant rewording"
    }
  ]
}
```

## Intensity Levels

- **light**: Minimal changes, preserves original meaning closely. Best for formal documents.
- **medium**: Balanced transformation for natural human style. Recommended for general use.
- **strong**: Significant rewording for maximum human-like quality. Best for creative content.

## Configuration

Edit `config.py` or `.env` to customize:
```env
HOST=127.0.0.1
PORT=8000
DEBUG=False
DEFAULT_INTENSITY=medium
MAX_BATCH_SIZE=100
MAX_TEXT_LENGTH=10000
```

## Testing

Run the test suite:
```bash
python test_api.py
```

Make sure the API is running in another terminal before running tests.

## Project Structure

```
ai-humanizer/
├── main.py              # FastAPI application
├── humanizer.py         # Core humanization engine
├── config.py            # Configuration settings
├── test_api.py          # API test suite
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
├── run.sh              # Linux/Mac startup script
├── run.bat             # Windows startup script
└── README.md           # This file
```

## How It Works

1. **Input Processing**: Receives AI-generated text
2. **Analysis**: Identifies AI-characteristic patterns (formal phrases, academic vocabulary, passive voice)
3. **Transformation**: Applies intensity-based transformations:
   - Phrase replacement (common AI patterns → natural alternatives)
   - Synonym substitution (formal words → conversational language)
   - Sentence restructuring (varies sentence structure)
4. **Output**: Returns humanized text with confidence score

## Examples

### Example 1: Light Intensity
**Input:**
```
The implementation of advanced technologies has demonstrated considerable efficacy in streamlining operational procedures.
```

**Output:**
```
The implementation of advanced technologies has shown real effectiveness in improving operational procedures.
```

### Example 2: Medium Intensity
**Input:**
```
Consequently, the paradigm shift necessitates comprehensive reassessment of existing frameworks.
```

**Output:**
```
So the shift in thinking requires a complete rethinking of current systems.
```

### Example 3: Strong Intensity
**Input:**
```
Fundamentally, leveraging cutting-edge methodologies facilitates unprecedented optimization opportunities in contemporary business landscapes.
```

**Output:**
```
Really, using new methods helps businesses find amazing improvement opportunities like never before.
```

## API Usage Examples

### Python
```python
import requests

response = requests.post(
    "http://localhost:8000/humanize",
    json={
        "text": "Your AI-generated text here",
        "intensity": "medium"
    }
)

result = response.json()
print(result["humanized"])
```

### cURL
```bash
curl -X POST "http://localhost:8000/humanize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your AI-generated text here",
    "intensity": "medium"
  }'
```

### JavaScript/Node.js
```javascript
const response = await fetch('http://localhost:8000/humanize', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: 'Your AI-generated text here',
    intensity: 'medium'
  })
});

const result = await response.json();
console.log(result.humanized);
```

## Requirements

See `requirements.txt` for dependencies:
- FastAPI >= 0.104.1
- Uvicorn >= 0.24.0
- Pydantic >= 2.5.0
- Python >= 3.8

## License

MIT

## Support

For issues or questions, please open an issue on GitHub.
