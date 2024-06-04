from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import pickle
import openai
import datetime
import random

app = FastAPI()

# Set up OpenAI API key
openai.api_key = 'your_openai_api_key'

class UserSession:
    def __init__(self, user_identifier, specialty):
        self.user_identifier = user_identifier
        self.specialty = specialty
        self.chat_history_file = f"{self.specialty}_{self.user_identifier}_chat.pkl"
        self.chat_history = []

    def save_chat_message(self, message):
        with open(self.chat_history_file, 'wb') as file:
            pickle.dump(self.chat_history, file)

    def load_chat_history(self):
        if os.path.exists(self.chat_history_file):
            with open(self.chat_history_file, 'rb') as file:
                self.chat_history = pickle.load(file)

    def clear_chat_history(self):
        if os.path.exists(self.chat_history_file):
            os.remove(self.chat_history_file)

class Message(BaseModel):
    user_id: str
    message: str

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    # Placeholder function, replace with actual implementation
    return len(string.split())

client = openai.OpenAI(api_key='your_openai_api_key')

def get_completion_from_messages(messages, model='gpt-3.5-turbo', temperature=0.8):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    response_bot = response.choices[0].message.content
    response_bot = response_bot.lower()
    print('********************************', response_bot)
    return response_bot

def start_session():
    print("Welcome to the medical chatbot!")
    print("Please select a specialty:")
    print("1. Cardio")
    print("2. Clinical Psychology")
    print("3. Dentistry")
    specialty_choice = input("Enter the number corresponding to your choice: ")
    specialties = {
        '1': 'Cardio',
        '2': 'Clinical Psychology',
        '3': 'Dentistry'
    }
    specialty = specialties.get(specialty_choice)
    if specialty:
        user_identifier = input("Enter a user identifier (e.g., A-user): ")
        session = UserSession(user_identifier, specialty)
        return session
    else:
        print("Invalid specialty choice.")
        return None

def get_user_input(prompt):
    return input(prompt + "\n")

def store_chat_message(session, message):
    session.save_chat_message(message)

def ask_patient_question(question):
    user_input = get_user_input(question)
    return user_input

def generate_medical_response(specialty, continuity_prompt):
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

def chat_interaction(session):
    if session:
        print(f"As a {session.specialty} specialist, I'm here to assist you.")

        session.load_chat_history()
        for message in session.chat_history:
            print(message.strip())

        clear_chat_option = input("Do you want to clear the previous chat and start a new session? (yes/no): ")
        if clear_chat_option.lower() == 'yes':
            session.clear_chat_history()
            print("Starting a new session.")

        questions = [
            "Can you share with me what you've been experiencing lately?",
            "Thank you for sharing that. Can you tell me more about what specifically triggers your mental health concern?",
            "How long have you been experiencing these symptoms?",
            "Have you noticed any patterns or changes in your daily routine that might be contributing to these feelings?"
        ]
        continuity_prompt = "Would you like to share more about your experiences or ask any specific questions?"

        # Asking the four hard-coded questions in a loop
        for question in questions:
            user_input = ask_patient_question(question)
            store_chat_message(session, f"User: {user_input}")

        # Generating medical response based on inputs
        response_suggestions = generate_medical_response(session.specialty, continuity_prompt)
        print("Bot: ", response_suggestions)

        # Looping for continuing or dumping the chat
        while True:
            options = ["1. Continue the conversation", "2. Dump the old chat and start a new session"]
            print("\n".join(options))
            choice = input("Enter the number corresponding to your choice: ")
            if choice == "1":
                user_input = ask_patient_question(continuity_prompt)
                store_chat_message(session, f"User: {user_input}")
                response_suggestions = generate_medical_response(session.specialty, continuity_prompt)
                print("Bot: ", response_suggestions)
            elif choice == "2":
                session.clear_chat_history()
                print("Starting a new session.")

                # Asking the four hard-coded questions in a loop for the new session
                for question in questions:
                    user_input = ask_patient_question(question)
                    store_chat_message(session, f"User: {user_input}")

                # Generating medical response based on inputs for the new session
                response_suggestions = generate_medical_response(session.specialty, continuity_prompt)
                print("Bot: ", response_suggestions)
    else:
        print("Session could not be started.")

@app.post("/careerchatbot")
async def chat_with_careerbot(message: Message):
    user_id = message.user_id
    message_text = message.message

    # Your chatbot logic here using UserSession and OpenAI API
    session = start_session()
    chat_interaction(session)

    return {"user_id": user_id, "message": message_text, "bot_response": "Bot's response"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
