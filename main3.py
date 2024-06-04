from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import openai
import datetime
import os

app = FastAPI()

# Set up OpenAI API key
openai.api_key = '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'

class UserSession:
    def __init__(self, user_identifier, specialty):
        self.user_identifier = user_identifier
        self.specialty = specialty
        self.chat_history = []

    def save_chat_message(self, message):
        self.chat_history.append({"role": "user", "content": message})

    def generate_medical_response(self, message):
        prompt_suggestions = f"""User: {message}

        Therapist Notes: Add a little bit information on which disorder patient is facing, one paragraph about the issue/disorder.
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

        Would you like to share more about your experiences or ask any specific questions?"""

        try:
            response_suggestions = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": prompt_suggestions}],
                max_tokens=1500
            )
            bot_response_suggestions = response_suggestions['choices'][0]['message']['content'].strip()
            self.chat_history.append({"role": "system", "content": bot_response_suggestions})
            return bot_response_suggestions

        except Exception as e:
            print(f"An error occurred while generating the response: {e}")
            return "Error generating response"

class UserInput(BaseModel):
    user_identifier: str
    message: str

@app.post("/chatbot/")
async def chatbot_endpoint(user_input: UserInput):
    user_identifier = user_input.user_identifier
    message = user_input.message

    session = UserSession(user_identifier, specialty="Medical")

    if message:
        session.save_chat_message(message)

    response = session.generate_medical_response(message)
    return {"Bot_Response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
