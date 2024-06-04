from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import datetime
import os
import random
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
            file.write(f"{datetime.datetime.now()} - {self.user_identifier}: {message}\n")

    def load_chat_history(self):
        if os.path.exists(self.chat_history_file):
            with open(self.chat_history_file, 'r') as file:
                self.chat_history = file.readlines()

    def clear_chat_history(self):
        if os.path.exists(self.chat_history_file):
            os.remove(self.chat_history_file)

class UserInput(BaseModel):
    user_id: str
    specialty: str
    message: Optional[str] = None

class BotResponse(BaseModel):
    response: str

session = None

@app.post("/chat/", response_model=BotResponse)
def chat_with_bot(user_input: UserInput):
    global session
    if not session:
        session = UserSession(user_input.user_id, user_input.specialty)

    if user_input.message:
        session.save_chat_message(user_input.message)

    if not user_input.message or user_input.message.lower() == "start":
        # Starting a new session or showing welcome message
        if not session:
            session = UserSession(user_input.user_id, user_input.specialty)
            return {"response": f"Welcome to the medical chatbot, {user_input.user_id}! Please start by sharing your experiences."}
        else:
            return {"response": "Your session is already active. Please continue sharing."}

    # Generating bot response
    bot_response = generate_medical_response(session.specialty, "Would you like to share more about your experiences or ask any specific questions?")
    return {"response": bot_response}

def generate_medical_response(specialty, continuity_prompt):
    # This function is taken from your previous code with minor modifications
    prompt_suggestions = f"""Therapist Notes: Add a little bit information on which disorder patient is facing, one paragraph about the issue/disorder.
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

    Add a little bit information on what exactly has happened to the patient 
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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
