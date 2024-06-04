from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import os

# Importing your existing code
import openai
import random

app = FastAPI(
    title="Medical Chatbot API",
    description="An API for starting a medical chatbot session.",
    version="1.0",
    docs_url="/",
)

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
        '1': 'Cardio',
        '2': 'Clinical Psychology',
        '3': 'Dentistry'
    }
    if request.specialty not in specialties.values():
        raise HTTPException(status_code=400, detail="Invalid specialty choice")

    # Use the 'prompt' parameter in your session initialization or processing logic
    session = UserSession(request.user_identifier, request.specialty)
    # Process the 'prompt' parameter as needed

    return {"message": "Session started successfully"}

import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)
