from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
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


class UserIdentifier(BaseModel):
    user_id: str
    specialty: str


class ChatMessage(BaseModel):
    message: str


class BotResponse(BaseModel):
    response: str


session = None


@app.post("/start_session/", response_model=BotResponse)
def start_user_session(user_info: UserIdentifier):
    global session
    session = UserSession(user_info.user_id, user_info.specialty)
    return {"response": "Session started successfully."}


@app.post("/send_message/", response_model=BotResponse)
def send_message(message_info: ChatMessage):
    global session
    if session:
        session.save_chat_message(message_info.message)
        return {"response": "Message saved successfully."}
    else:
        raise HTTPException(status_code=400, detail="Session not started.")


@app.post("/get_bot_response/", response_model=BotResponse)
def get_bot_response():
    global session
    if session:
        # Your code for generating bot response goes here
        response_suggestions = "Sample bot response"
        return {"response": response_suggestions}
    else:
        raise HTTPException(status_code=400, detail="Session not started.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

