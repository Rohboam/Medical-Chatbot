import openai
import datetime

# Set up OpenAI API key
openai.api_key = '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'

class UserSession:
    def __init__(self, specialty):
        self.specialty = specialty
        self.chat_history = []  # List to store chat messages

    def add_message(self, message):
        self.chat_history.append(message)

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
        session = UserSession(specialty)
        return session
    else:
        print("Invalid specialty choice.")
        return None 

def get_user_input():
    return input("User: ")

def store_chat_message(session, message):
    session.add_message(message)

def ask_patient_question(question, session):
    print(question)
    user_input = get_user_input()
    store_chat_message(session, {'timestamp': datetime.datetime.now(), 'content': user_input})
    return user_input

def generate_medical_response(chat_history, specialty):
    # Extract user input from chat history
    patient_concern = chat_history[0]['content']
    trigger = chat_history[1]['content']
    symptoms_duration = chat_history[2]['content']
    daily_changes = chat_history[3]['content']

    # Build the prompt for professional suggestions
    prompt_suggestions = f"""Therapist Notes: Add a little bit information on which disorder patient is facing, one paragarph about the issue/disorder.
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

    Add a little bit information on what exactly has happened to patient 
    - one paragarph about the issue/disorder

    Additionally, I suggest some authentic journal articles/publications related to issue you are facing:
    - [Article name/discription]
    - [Article name/discription]
    - [Article name/discription]

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
        
        # Check if chat history is empty before proceeding
        if not session.chat_history:
            questions = [
                "Can you share with me what you've been experiencing lately?",
                "Thank you for sharing that. Can you tell me more about what specifically triggers your mental health concern?",
                "How long have you been experiencing these symptoms?",
                "Have you noticed any patterns or changes in your daily routine that might be contributing to these feelings?"
            ]
            
            for question in questions:
                user_input = ask_patient_question(question, session)
        
        response_suggestions = generate_medical_response(session.chat_history, session.specialty)
        print("AI Suggestions: ", response_suggestions)

    else:
        print("Session could not be started.")

session = start_session()
chat_interaction(session)
