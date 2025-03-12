from pathlib import Path
import os
import json
import requests
from fastapi import FastAPI, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import openai
import asyncio
import time
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# T2A API settings
T2A_API_KEY = os.getenv("T2A_API_KEY")
T2A_GROUP_ID = os.getenv("T2A_GROUP_ID")
T2A_URL = "https://api.t2a.ai/v1/tts"

# Initialize FastAPI
app = FastAPI()

# Setup static file serving
STATIC_DIR = Path(__file__).parent / "static"
AUDIO_DIR = STATIC_DIR / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

async def simplify_and_translate(text: str) -> dict:
    """Simplify and translate text for children using OpenAI"""
    try:
        # Create a child-friendly explanation in English
        response = await openai.ChatCompletion.acreate(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": "You are an expert at explaining complex concepts to 5-year-old Ugandan children. Use simple words, cultural references they understand, and engaging examples. Focus on making learning easy and fun so children can grasp concepts easily."},
                {"role": "user", "content": f"Explain this concept in simple terms that a 5-year-old Ugandan child would understand: {text}"}
            ]
        )
        simplified = response.choices[0].message['content'].strip()
        
        # Translate to Luganda
        response = await openai.ChatCompletion.acreate(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": "You are a professional translator specializing in translating English to Luganda for children. Keep the translation simple and natural."},
                {"role": "user", "content": f"Translate this child-friendly explanation to Luganda: {simplified}"}
            ]
        )
        translated = response.choices[0].message['content'].strip()
        
        return {
            "simplified": simplified,
            "translated": translated
        }
    except Exception as e:
        print(f"OpenAI API error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process text")

@app.post("/translate")
async def translate_text(text: str = Form(...)):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Get text translations
    result = await simplify_and_translate(text)
    
    try:
        # Ensure audio directory exists
        AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        timestamp = int(time.time())
        filename = f"speech_{timestamp}.mp3"
        audio_file = AUDIO_DIR / filename
        
        # Try gTTS first since it's more reliable
        try:
            tts = gTTS(text=result["simplified"], lang='en', slow=True)
            tts.save(str(audio_file))
            
            if not audio_file.exists() or audio_file.stat().st_size == 0:
                raise Exception("Failed to generate audio with gTTS")
                
        except Exception as e:
            print(f"gTTS failed: {str(e)}, trying T2A API")
            
            # Try T2A API as fallback
            url = f"{T2A_URL}?GroupId={T2A_GROUP_ID}"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {T2A_API_KEY}"
            }
            
            data = {
                "text": result["simplified"],
                "voice_id": "nova",
                "speed": 0.85
            }
            
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                result_audio = response.json()
                if "data" in result_audio and "audio" in result_audio["data"]:
                    audio_data = bytes.fromhex(result_audio["data"]["audio"])
                    audio_file.write_bytes(audio_data)
                else:
                    raise Exception("Invalid T2A API response format")
            else:
                raise Exception(f"T2A API error: {response.text}")
        
        # Verify final audio file
        if not audio_file.exists() or audio_file.stat().st_size == 0:
            raise Exception("Failed to generate audio file")
            
        audio_url = f"/static/audio/{filename}"
        
    except Exception as e:
        print(f"Audio generation error: {str(e)}")
        audio_url = None
    
    return {
        "original": text,
        "simplified": result["simplified"],
        "translated": result["translated"],
        "audio_url": audio_url
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8201))
    uvicorn.run(app, host="0.0.0.0", port=port)
