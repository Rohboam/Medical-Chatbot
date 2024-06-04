import openai
import datetime
import os

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

def start_session():
    print("Welcome to the clinical psychology chatbot!")
    user_identifier = input("Enter a user identifier (e.g., A-user): ")
    session = UserSession(user_identifier, "ClinicalPsychology")  # Specialty set directly
    return session

def get_user_input(prompt):
    return input(prompt + "\n")

def store_chat_message(session, message):
    session.save_chat_message(message)

def ask_patient_question(question):
    user_input = get_user_input(question)
    return user_input

def generate_psychological_response(continuity_prompt):
    prompt_suggestions = f"""Therapist: Thank you for sharing. Based on what you've described, here are some strategies we can consider to address your concerns together:
    1. [Strategy 1]
    2. [Strategy 2]
    3. [Strategy 3]

    I suggest exploring the following resources or activities that may be helpful for you:
    - [Resource/activity 1]
    - [Resource/activity 2]
    - [Resource/activity 3]

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

        clear_chat_option = input("Do you want to clear the previous chat and start a new session? (yes/no): ")
        if clear_chat_option.lower() == 'yes':
            session.clear_chat_history()
            print("Starting a new session.")

        continuity_prompt = "Would you like to share more about your experiences or ask any specific questions?"

        while True:
            user_input = ask_patient_question(continuity_prompt)
            store_chat_message(session, f"User: {user_input}")
            response_suggestions = generate_psychological_response(continuity_prompt)
            print("Bot: ", response_suggestions)

            option = input("Do you want to continue the conversation? (yes/no): ")
            if option.lower() != 'yes':
                break
    else:
        print("Session could not be started.")

session = start_session()
chat_interaction(session)
