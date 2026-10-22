import os
import time
import requests
from flask import Flask, render_template, request, jsonify, url_for
from dotenv import load_dotenv
from google import genai
from gtts import gTTS

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Ensure output directories exist
OUTPUT_DIR = "static/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize Gemini Client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def generate_story_and_prompt(topic):
    """Uses Gemini API to generate a short narration story and an image prompt."""
    if not client:
        # Fallback dummy narrative if no API key provided
        return (
            f"Once upon a time in a distant realm, {topic} created a breathtaking spectacle of light and shadow.",
            f"Artistic painting of {topic}, vibrant colors, ultra detailed, cinematic lighting"
        )
    
    system_prompt = (
        "You are a creative curator for digital art experiences. "
        "Given a topic, return EXACTLY two lines separated by '|||':\n"
        "Line 1: A 2-sentence poetic story narration.\n"
        "Line 2: A vivid visual image prompt describing artwork representing the story."
    )
    
    response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=f"{system_prompt}\n\nTopic: {topic}"
)
    
    text = response.text.strip()
    if "|||" in text:
        parts = text.split("|||")
        narration = parts[0].strip()
        image_prompt = parts[1].strip()
    else:
        narration = text
        image_prompt = f"Digital artwork depicting {topic}, highly detailed, 4k"
        
    return narration, image_prompt


def generate_image(prompt, timestamp):
    """Generates a static artwork image from the prompt using Pollinations AI."""
    # Pollinations AI generates images directly via URL prompt endpoint
    clean_prompt = requests.utils.quote(prompt)
    image_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width=800&height=800&seed={timestamp}&nologo=true"
    
    response = requests.get(image_url)
    if response.status_code == 200:
        filename = f"art_{timestamp}.jpg"
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return f"outputs/{filename}"
    else:
        raise Exception("Failed to generate image from AI service.")


def generate_audio(text, timestamp):
    """Converts the story text into spoken voice audio (MP3) using gTTS."""
    tts = gTTS(text=text, lang='en', slow=False)
    filename = f"narration_{timestamp}.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)
    tts.save(filepath)
    return f"outputs/{filename}"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate-experience', methods=['POST'])
def generate_experience():
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        
        if not topic:
            return jsonify({'success': False, 'error': 'Please enter a topic or theme.'}), 400
        
        timestamp = int(time.time())
        
        # Step 1: Generate Story & Image Prompt using Gemini
        narration, image_prompt = generate_story_and_prompt(topic)
        
        # Step 2: Generate Art Image
        image_relative_path = generate_image(image_prompt, timestamp)
        
        # Step 3: Generate Voice Narration Audio
        audio_relative_path = generate_audio(narration, timestamp)
        
        return jsonify({
            'success': True,
            'narration': narration,
            'image_prompt': image_prompt,
            'image_url': url_for('static', filename=image_relative_path),
            'audio_url': url_for('static', filename=audio_relative_path)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)