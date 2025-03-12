# English to Luganda Academic Concepts Translator

This application helps explain academic concepts to children by translating them from English to Luganda with audio output. It uses advanced AI to simplify complex concepts and provide accurate Luganda translations.

## Features

- Simplified explanations for 5-year-olds
- High-quality Luganda translations using GPT-4
- Audio output for translations
- Child-friendly web interface
- Fast response times with dual AI system

## Technical Details

### AI Translation System
- Primary explanation: DeepSeek AI (with 15s timeout)
- Fallback explanation: OpenAI GPT-4
- Luganda translation: OpenAI GPT-4 with specialized prompting
- Audio: Google Translate TTS

### Dependencies
```bash
fastapi==0.95.0
uvicorn==0.21.1
python-multipart==0.0.6
openai==1.3.0
python-dotenv==0.21.1
jinja2==3.1.2
requests==2.31.0
```

## Setup Instructions

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your API keys:
   - DeepSeek API key
   - OpenAI API key (with GPT-4 access)

3. Run the application:
```bash
python main.py
```

4. Open your browser and visit `http://localhost:8080`

## How It Works

1. **Concept Simplification:**
   - First attempts to use DeepSeek AI
   - If DeepSeek takes too long (>15s), switches to GPT-4
   - Explains concepts in simple, child-friendly English

2. **Luganda Translation:**
   - Uses GPT-4 with specialized prompting for accurate Luganda translations
   - Maintains cultural context and proper grammar
   - Handles academic terms appropriately

3. **Audio Generation:**
   - Converts Luganda text to speech
   - No API key required
   - Clear and natural pronunciation

## Usage

1. Enter any academic concept in English
2. Click "Translate and Explain!"
3. View the simplified explanation
4. Read the Luganda translation
5. Listen to the audio pronunciation

## Note

This application requires an active internet connection for AI services and text-to-speech functionality.
