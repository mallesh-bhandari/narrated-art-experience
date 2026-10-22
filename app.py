import os
import time
import requests
from flask import Flask, render_template, request, jsonify, url_for
from dotenv import load_dotenv
from google import genai
from gtts import gTTS

# =====================================================================
# 1. APPLICATION SETUP & CONFIGURATION
# =====================================================================

# Load secret environment variables (like API keys) from the .env file
load_dotenv()

# Initialize the Flask web application instance
app = Flask(__name__)

# Define and create the local directory where generated images and audio files are stored
OUTPUT_DIR = "static/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize the official Google GenAI Client using the API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


# =====================================================================
# 2. AI CONTENT GENERATION PIPELINE (Google Gemini API)
# =====================================================================

def generate_story_and_prompt(topic):
    """Uses Gemini API to generate a short narration story and an image prompt."""
    
    # Fallback mechanism if the API key is missing or client isn't initialized
    if not client:
        return (
            f"Once upon a time in a distant realm, {topic} created a breathtaking spectacle of light and shadow.",
            f"Artistic painting of {topic}, vibrant colors, ultra detailed, cinematic lighting"
        )
    
    # System instructions defining how Gemini should format its output
    system_prompt = (
        "You are a creative curator for digital art experiences. "
        "Given a topic, return EXACTLY two lines separated by '|||':\n"
        "Line 1: A 2-sentence poetic story narration.\n"
        "Line 2: A vivid visual image prompt describing artwork representing the story."
    )
    
    # Call the Gemini model to generate content based on the user's topic
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=f"{system_prompt}\n\nTopic: {topic}"
    )
    
    text = response.text.strip()
    
    # Parse the response text using the '|||' separator to split story and image prompt
    if "|||" in text:
        parts = text.split("|||")
        narration = parts[0].strip()
        image_prompt = parts[1].strip()
    else:
        # Fallback parsing if the model layout varies slightly
        narration = text
        image_prompt = f"Digital artwork depicting {topic}, highly detailed, 4k"
        
    return narration, image_prompt


# =====================================================================
# 3. VISUAL ART GENERATION PIPELINE (Pollinations AI)
# =====================================================================

def generate_image(prompt, timestamp):
    """Generates a static artwork image from the prompt using Pollinations AI."""
    
    # URL-encode the text prompt so it can safely pass through HTTP requests
    clean_prompt = requests.utils.quote(prompt)
    
    # Construct the dynamic image URL pointing to Pollinations AI service
    image_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width=800&height=800&seed={timestamp}&nologo=true"
    
    # Send HTTP GET request to fetch the generated image content
    response = requests.get(image_url)
    
    if response.status_code == 200:
        # Create a unique filename using the timestamp
        filename = f"art_{timestamp}.jpg"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Save the binary image content locally into the static outputs folder
        with open(filepath, 'wb') as f:
            f.write(response.content)
            
        return f"outputs/{filename}"
    else:
        raise Exception("Failed to generate image from AI service.")


# =====================================================================
# 4. VOICE NARRATION PIPELINE (gTTS - Text to Speech)
# =====================================================================

def generate_audio(text, timestamp):
    """Converts the story text into spoken voice audio (MP3) using gTTS."""
    
    # Initialize Google Text-to-Speech engine with English language and normal speed
    tts = gTTS(text=text, lang='en', slow=False)
    
    # Define unique filename and path for the output audio file
    filename = f"narration_{timestamp}.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # Save the synthesized audio file locally
    tts.save(filepath)
    
    return f"outputs/{filename}"


# =====================================================================
# 5. FLASK WEB ROUTES & CONTROLLERS
# =====================================================================

@app.route('/')
def index():
    """Renders the main frontend user interface homepage."""
    return render_template('index.html')


@app.route('/generate-experience', methods=['POST'])
def generate_experience():
    """API endpoint that orchestrates the entire generation pipeline."""
    try:
        # Extract JSON data sent from the frontend request
        data = request.get_json()
        topic = data.get('topic', '').strip()
        
        # Validate that the user actually entered a topic
        if not topic:
            return jsonify({'success': False, 'error': 'Please enter a topic or theme.'}), 400
        
        # Generate a unique timestamp ID to prevent asset caching conflicts
        timestamp = int(time.time())
        
        # -------------------------------------------------------------
        # Step 1: Generate Story Narration & Image Prompt via Gemini API
        # -------------------------------------------------------------
        narration, image_prompt = generate_story_and_prompt(topic)
        
        # -------------------------------------------------------------
        # Step 2: Generate and Save Visual Artwork Image via Pollinations
        # -------------------------------------------------------------
        image_relative_path = generate_image(image_prompt, timestamp)
        
        # -------------------------------------------------------------
        # Step 3: Generate and Save Voice Narration Audio File via gTTS
        # -------------------------------------------------------------
        audio_relative_path = generate_audio(narration, timestamp)
        
        # Return all generated assets and URLs back to the frontend UI as JSON
        return jsonify({
            'success': True,
            'narration': narration,
            'image_prompt': image_prompt,
            'image_url': url_for('static', filename=image_relative_path),
            'audio_url': url_for('static', filename=audio_relative_path)
        })
        
    except Exception as e:
        # Catch and return any errors gracefully to the frontend UI
        return jsonify({'success': False, 'error': str(e)}), 500


# =====================================================================
# 6. APPLICATION ENTRY POINT
# =====================================================================

if __name__ == '__main__':
    # Run the Flask development server on all network interfaces at port 5000
    app.run(host='0.0.0.0', port=5000)