# main.py - FastAPI Backend
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from typing import Dict, Any
import uvicorn

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Equanimity API",
    description="AI-powered equanimity assessment and practice generator",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Streamlit domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini AI
try:
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    print(f"Warning: Gemini AI configuration failed: {e}")
    model = None

# Pydantic models
class AssessmentAnswers(BaseModel):
    answers: Dict[str, str]

class TechniqueResponse(BaseModel):
    technique_title: str
    description: str
    insight: str
    day1: Dict[str, str]
    day2: Dict[str, str]
    day3: Dict[str, str]
    zen_quote: str
    long_term_guidance: str

@app.get("/")
async def root():
    return {"message": "Equanimity API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "gemini_configured": model is not None,
        "api_version": "1.0.0"
    }

@app.post("/generate-technique", response_model=TechniqueResponse)
async def generate_technique(assessment: AssessmentAnswers):
    """
    Generate a personalized 3-day equanimity practice based on assessment answers
    """
    if not model:
        raise HTTPException(
            status_code=500, 
            detail="AI model not configured. Please check GEMINI_API_KEY environment variable."
        )
    
    try:
        # Extract keywords from all answers
        all_keywords = []
        for answer_keywords in assessment.answers.values():
            all_keywords.extend(answer_keywords.split(', '))
        
        # Create detailed prompt for Gemini
        prompt = f"""
You are a renowned Buddhist meditation teacher and mindfulness coach with deep expertise in equanimity practices. Based on this psychological profile from a 5-question assessment, create a transformative 3-day equanimity practice.

ASSESSMENT KEYWORDS: {', '.join(all_keywords)}

The user's responses reveal their current patterns with:
1. Stress response and challenge management
2. Reception of criticism and feedback
3. Emotional regulation and awareness
4. Control, surrender, and acceptance
5. Relationship with pleasure/pain, success/failure

Create a response in this EXACT JSON format (no additional text):

{{
    "technique_title": "A poetic, inspiring name for the practice (4-8 words)",
    "description": "2-3 sentences explaining why this practice perfectly suits their current state and how it will cultivate deep equanimity",
    "insight": "One profound, personally relevant insight about equanimity that speaks directly to their patterns",
    "day1": {{
        "title": "Foundation theme (2-3 words like 'Grounding Awareness')",
        "morning_practice": "Detailed 10-15 minute morning practice with step-by-step instructions",
        "daily_integration": "Specific techniques to apply throughout the day, with concrete examples",
        "evening_reflection": "5-10 minute evening practice with clear guidance"
    }},
    "day2": {{
        "title": "Deepening theme (2-3 words like 'Expanding Presence')", 
        "morning_practice": "Building on day 1, slightly more advanced morning practice",
        "daily_integration": "Deeper integration techniques for real-life challenges",
        "evening_reflection": "More sophisticated evening practice for integration"
    }},
    "day3": {{
        "title": "Integration theme (2-3 words like 'Embodied Wisdom')",
        "morning_practice": "Most refined version connecting to their natural equanimity",
        "daily_integration": "How to make equanimity a permanent life orientation",
        "evening_reflection": "Celebration practice and commitment to ongoing development"
    }},
    "zen_quote": "A relevant, inspiring quote from Buddhist tradition that resonates with their specific journey",
    "long_term_guidance": "Practical advice for maintaining and deepening this practice beyond 3 days, tailored to their patterns"
}}

Requirements:
- Make it deeply personal and transformative
- Use practical, actionable techniques they can actually implement
- Draw from Vipassana, Zen, Tibetan Buddhism while staying accessible
- Address their specific emotional/mental patterns revealed in keywords
- Build progressively over 3 days toward lasting transformation
- Include specific meditation techniques, breathing practices, mindfulness exercises
- Provide concrete examples of how to apply teachings in daily situations

Focus on creating genuine wisdom that leads to freedom from reactivity and the development of unshakeable inner peace.
"""

        # Generate response from Gemini
        response = model.generate_content(prompt)
        
        # Parse the JSON response
        try:
            # Clean the response text (remove markdown formatting if present)
            clean_response = response.text.strip()
            if clean_response.startswith('```json'):
                clean_response = clean_response[7:]
            if clean_response.endswith('```'):
                clean_response = clean_response[:-3]
            clean_response = clean_response.strip()
            
            technique_data = json.loads(clean_response)
            
            # Validate the response structure
            required_fields = ['technique_title', 'description', 'insight', 'day1', 'day2', 'day3', 'zen_quote', 'long_term_guidance']
            for field in required_fields:
                if field not in technique_data:
                    raise ValueError(f"Missing required field: {field}")
            
            return TechniqueResponse(**technique_data)
            
        except (json.JSONDecodeError, ValueError) as parse_error:
            print(f"JSON parsing error: {parse_error}")
            print(f"Raw response: {response.text}")
            
            # Return a fallback response
            return TechniqueResponse(
                technique_title="The Path of Present Awareness",
                description="Based on your responses, you would benefit from a practice that cultivates moment-to-moment awareness and emotional balance. This gentle yet powerful approach will help you develop equanimity through mindful presence.",
                insight="True equanimity arises not from avoiding life's challenges, but from meeting them with an open, spacious heart that remains unchanged by changing circumstances.",
                day1={
                    "title": "Grounding Practice",
                    "morning_practice": "Begin with 10 minutes of breath awareness. Sit comfortably, close your eyes, and simply observe your natural breathing. When thoughts arise, gently return to the breath without judgment.",
                    "daily_integration": "Throughout the day, take three conscious breaths before responding to any challenging situation. This creates space between stimulus and response.",
                    "evening_reflection": "Before sleep, reflect on one moment when you remained calm during difficulty, appreciating your natural capacity for peace."
                },
                day2={
                    "title": "Expanding Awareness",
                    "morning_practice": "Practice loving-kindness meditation for 15 minutes. Begin with yourself, then extend compassion to loved ones, neutral people, difficult people, and all beings.",
                    "daily_integration": "When facing criticism or conflict, silently wish the other person well while maintaining your center. Notice how this changes your internal experience.",
                    "evening_reflection": "Journal about how extending compassion affected your sense of inner stability and connection."
                },
                day3={
                    "title": "Embodied Wisdom",
                    "morning_practice": "Sit in open awareness for 15 minutes. Rest in spacious consciousness, aware of thoughts and feelings arising and passing without attachment.",
                    "daily_integration": "Practice seeing all experiences as temporary weather patterns in the sky of awareness. You are the sky, not the weather.",
                    "evening_reflection": "Set an intention to continue cultivating equanimity, knowing that each moment offers a fresh opportunity to practice."
                },
                zen_quote="Peace comes from within. Do not seek it without. - Buddha",
                long_term_guidance="Continue daily meditation practice, even if just 5-10 minutes. Remember that equanimity is not a destination but a way of traveling through life with grace and wisdom."
            )
            
    except Exception as e:
        print(f"API Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate technique: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )