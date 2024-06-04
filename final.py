from fastapi import FastAPI, HTTPException, Query, Path, Body
from pydantic import BaseModel
from datetime import datetime
import os
import openai

app = FastAPI()

# Set up OpenAI API key
openai.api_key = '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'

class UserSession:
    def __init__(self, user_identifier, specialty):
        self.user_identifier = user_identifier
        self.specialty = specialty
        self.chat_history_file = f"{self.specialty}_{self.user_identifier}_chat.txt"
        self.chat_history = []

    def save_chat_message(self, message):
        with open(self.chat_history_file, 'a') as file:
            file.write(f"{datetime.now()} - {self.user_identifier}: {message}\n")

    def load_chat_history(self):
        if os.path.exists(self.chat_history_file):
            with open(self.chat_history_file, 'r') as file:
                self.chat_history = file.readlines()

    def clear_chat_history(self):
        if os.path.exists(self.chat_history_file):
            os.remove(self.chat_history_file)

class StartSessionRequest(BaseModel):
    user_identifier: str
    specialty: str
    prompt: str

class ChatMessage(BaseModel):
    message: str

def generate_medical_response(specialty, continuity_prompt):
    prompt_suggestions = f"""Therapist Notes: Add a little bit of information on which disorder the patient is facing, one paragraph about the issue/disorder.
    Therapist: Thank you for sharing. Based on what you've described, here are some strategies we can consider to address your concerns together:
    1. [Strategy 1]
    2. [Strategy 2]
    3. [Strategy 3]

    Medications to consider based on your condition:
    1. [Medication 1]
    2. [Medication 2]
    3. [Medication 3]

    I suggest exploring the following resources or activities that may be helpful for you:
    - [Resource/activity 1]
    - [Resource/activity 2]
    - [Resource/activity 3]

    Add a little bit of information on what exactly has happened to the patient 
    - one paragraph about the issue/disorder

    Additionally, I suggest some authentic journal articles/publications related to the issue you are facing:
    - [Article name/description]
    - [Article name/description]
    - [Article name/description]

    Let's work together on implementing these strategies and monitoring your progress. Your well-being is our priority.

    {continuity_prompt}"""

    max_tokens_suggestions = 1500
    try:
        response_suggestions = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt_suggestions}],
            max_tokens=max_tokens_suggestions
        )
        bot_response_suggestions = response_suggestions['choices'][0]['message']['content'].strip()

        return bot_response_suggestions

    except Exception as e:
        print(f"An error occurred while generating the response: {e}")
        return "Error generating response"

@app.post("/start_session/", response_model=dict, tags=["Session"])
async def start_session(request: StartSessionRequest):
    """
    Start a new session for the user.

    Parameters:
    - request: Request body containing user identifier, specialty, and prompt.

    Returns:
    - message: A message indicating whether the session started successfully.
    """
    specialties = {
        'Cardio': '1',
        'Clinical Psychology': '2',
        'Dentistry': '3'
    }
    if request.specialty not in specialties:
        raise HTTPException(status_code=400, detail="Invalid specialty choice")

    session = UserSession(request.user_identifier, request.specialty)
    return {"message": "Session started successfully"}

@app.post("/chat_interaction/{user_identifier}/{specialty}/", response_model=str, tags=["Chat"])
async def chat_interaction(user_identifier: str, specialty: str, message: ChatMessage):
    """
    Simulate chat interaction with the medical chatbot.

    Parameters:
    - user_identifier: The user's identifier.
    - specialty: The specialty chosen for the session.
    - message: The user's message.

    Returns:
    - bot_response: The response from the chatbot.
    """
    session = UserSession(user_identifier, specialty)
    session.load_chat_history()

    store_chat_message(session, f"User: {message.message}")
    response_suggestions = generate_medical_response(specialty, "Continuity prompt")
    store_chat_message(session, f"Bot: {response_suggestions}")

    return response_suggestions

def store_chat_message(session, message):
    session.save_chat_message(message)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
