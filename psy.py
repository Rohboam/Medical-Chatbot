import openai
import datetime
import os  # Import os module to check file existence

# Set up OpenAI API key
openai.api_key = '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'

class UserSession:
    def __init__(self, user_identifier, specialty):
        self.user_identifier = user_identifier
        self.specialty = specialty
        self.chat_history = []  # Initialize chat history list

    def save_chat_message(self, message):
        file_name = f"{self.specialty}_chat.txt"
        with open(file_name, 'a') as file:
            file.write(f"{datetime.datetime.now()} - {self.user_identifier}: {message}\n")

    def load_chat_history(self):
        file_name = f"{self.specialty}_chat.txt"
        if os.path.exists(file_name):  # Check if file exists
            with open(file_name, 'r') as file:
                self.chat_history = file.readlines()
        else:
            print(f"No chat history found for {self.specialty}. Starting a new conversation.")

    def clear_chat_history(self):
        file_name = f"{self.specialty}_chat.txt"
        if os.path.exists(file_name):  # Check if file exists
            os.remove(file_name)
            print(f"Chat history deleted for {self.specialty}.")
        else:
            print(f"No chat history found for {self.specialty}.")

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
    return input(prompt)

def store_chat_message(session, message):
    session.save_chat_message(message)

def ask_patient_question(question):
    print(question)
    user_input = get_user_input("User: ")
    return user_input

def generate_medical_response(specialty):
    # Build the prompt for professional suggestions
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

    Let's work together on implementing these strategies and monitoring your progress. Your well-being is our priority."""

    max_tokens_suggestions = 1500  # Increase the max_tokens for suggestions
    try:
        # Generate response for patient's suggestions
        response_suggestions = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use GPT-3.5 Turbo engine
            messages=[{"role": "system", "content": prompt_suggestions}],
            max_tokens=max_tokens_suggestions
        )
        bot_response_suggestions = response_suggestions['choices'][0]['message']['content'].strip()

        return bot_response_suggestions  # Return only suggestions

    except Exception as e:
        print(f"An error occurred while generating the response: {e}")
        return "Error generating response"

def chat_interaction(session):
    if session:
        print(f"As a {session.specialty} specialist, I'm here to assist you.")

        # Load previous chat history if available
        session.load_chat_history()
        for message in session.chat_history:
            print(message.strip())  # Strip newline characters

        # Prompt user to clear chat history and start a new session
        clear_chat_option = input("Do you want to clear the previous chat and start a new session? (yes/no): ")
        if clear_chat_option.lower() == 'yes':
            session.clear_chat_history()
            print("Starting a new session.")

        while True:
            # Ask the initial set of questions
            questions = [
                "Can you share with me what you've been experiencing lately?",
                "Thank you for sharing that. Can you tell me more about what specifically triggers your mental health concern?",
                "How long have you been experiencing these symptoms?",
                "Have you noticed any patterns or changes in your daily routine that might be contributing to these feelings?"
            ]
            for question in questions:
                user_input = ask_patient_question(question)
                store_chat_message(session, f"User: {user_input}")
                
                # Generate medical response and show options
                response_suggestions = generate_medical_response(session.specialty)
                print("Bot: ", response_suggestions)
                options = ["1. Continue the conversation", "2. End the conversation"]
                print("\n".join(options))
                choice = input("Enter the number corresponding to your choice: ")
                if choice == "2":
                    print("Ending the conversation.")
                    return  # End the conversation

            # Ask engaging trailing question
            trailing_question = "Would you like to share more about your experiences or ask any specific questions?"
            user_input = ask_patient_question(trailing_question)
            store_chat_message(session, f"User: {user_input}")

            # Check if user wants to continue or end the conversation
            options = ["1. Continue the conversation", "2. End the conversation"]
            print("\n".join(options))
            choice = input("Enter the number corresponding to your choice: ")
            if choice == "2":
                print("Ending the conversation.")
                return  # End the conversation
    else:
        print("Session could not be started.")




session = start_session()
chat_interaction(session)
