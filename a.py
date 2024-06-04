import openai
import datetime
import os
import random

# Set up OpenAI API key
openai.api_key = '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'


class UserSession:
    def __init__(self, user_identifier, specialty):
        self.user_identifier = user_identifier
        self.specialty = specialty
        self.chat_history_file = f"{self.specialty}_{self.user_identifier}_chat.txt"
        self.chat_history = []

    def save_chat_message(self, role, message):
        with open(self.chat_history_file, 'a') as file:
            file.write(f"{datetime.datetime.now()} - {role}: {message}\n")
        self.chat_history.append((role, message))  # Append to chat history

    def load_chat_history(self):
        if os.path.exists(self.chat_history_file):
            with open(self.chat_history_file, 'r') as file:
                self.chat_history = [line.strip() for line in file.readlines()]

    def clear_chat_history(self):
        if os.path.exists(self.chat_history_file):
            os.remove(self.chat_history_file)
            self.chat_history = []  # Reset chat history when cleared

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

def get_user_input(prompt):
    return input(prompt + "\n")


def ask_patient_question(question):
    user_input = get_user_input(question)
    return user_input

def store_chat_message(session, role, message):
    session.save_chat_message(role, message)


def summarize_chat(session):
    if not session.chat_history:
        return "No chat history available for summarization."

    user_messages = []
    bot_messages = []
    for message in session.chat_history:
        if ": " in message:
            split_message = message.split(": ", 1)
            if len(split_message) == 2:
                role, content = split_message
                if role.strip() == "User":
                    user_messages.append(content.strip())
                elif role.strip() == "Bot":
                    bot_messages.append(content.strip())

    user_summary = "\n".join(user_messages)
    bot_summary = "\n".join(bot_messages)

    summary = f"User's messages:\n{user_summary}\n\nBot's messages:\n{bot_summary}\n\n"
    
    return summary




def generate_medical_response(specialty, continuity_prompt, session):
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

        chat_summary = summarize_chat(session)
        return bot_response_suggestions + "\n" + chat_summary

    except Exception as e:
        print(f"An error occurred while generating the response: {e}")
        return "Error generating response"

# def chat_interaction(session):
#     if session:
#         print(f"As a {session.specialty} specialist, I'm here to assist you.")

#         session.load_chat_history()
#         for message in session.chat_history:
#             print(message.strip())

#         clear_chat_option = input("Do you want to clear the previous chat and start a new session? (yes/no): ")
#         if clear_chat_option.lower() == 'yes':
#             session.clear_chat_history()
#             print("Starting a new session.")

#         questions = [
#             "Can you share with me what you've been experiencing lately?",
#             "Thank you for sharing that. Can you tell me more about what specifically triggers your mental health concern?",
#             "How long have you been experiencing these symptoms?",
#             "Have you noticed any patterns or changes in your daily routine that might be contributing to these feelings?"
#         ]
#         continuity_prompt = "Would you like to share more about your experiences or ask any specific questions?"

#         # Asking the four hard-coded questions in a loop
#         for question in questions:
#             user_input = ask_patient_question(question)
#             store_chat_message(session, "User", user_input)

#         # Generating medical response based on inputs
#         response_suggestions = generate_medical_response(session.specialty, continuity_prompt, session)
#         store_chat_message(session, "Bot", response_suggestions)  # Save bot response
#         print("Bot: ", response_suggestions)

#         # Looping for continuing or dumping the chat
#         while True:
#             options = ["1. Continue the conversation", "2. Dump the old chat and start a new session"]
#             print("\n".join(options))
#             choice = input("Enter the number corresponding to your choice: ")
#             if choice == "1":
#                 user_input = ask_patient_question(continuity_prompt)
#                 store_chat_message(session, "User", user_input)
#                 response_suggestions = generate_medical_response(session.specialty, continuity_prompt, session)
#                 store_chat_message(session, "Bot", response_suggestions)  # Save bot response
#                 print("Bot: ", response_suggestions)
#             elif choice == "2":
#                 session.clear_chat_history()
#                 print("Starting a new session.")

#                 # Asking the four hard-coded questions in a loop for the new session
#                 for question in questions:
#                     user_input = ask_patient_question(question)
#                     store_chat_message(session, "User", user_input)

#                 # Generating medical response based on inputs for the new session
#                 response_suggestions = generate_medical_response(session.specialty, continuity_prompt, session)
#                 store_chat_message(session, "Bot", response_suggestions)  # Save bot response
#                 print("Bot: ", response_suggestions)
#     else:
#         print("Session could not be started.")

def chat_interaction(session):
    if session:
        print(f"As a {session.specialty} specialist, I'm here to assist you.")

        questions = [
            "Can you share with me what you've been experiencing lately?",
            "Thank you for sharing that. Can you tell me more about what specifically triggers your mental health concern?",
            "How long have you been experiencing these symptoms?",
            "Have you noticed any patterns or changes in your daily routine that might be contributing to these feelings?"
        ]
        continuity_prompt = "Would you like to share more about your experiences or ask any specific questions?"

        # Check if there's existing chat history
        session.load_chat_history()
        if session.chat_history:
            print("Previous chat history detected. Would you like to view the chat summary? (yes/no)")
            view_summary = input("Enter your choice: ")
            if view_summary.lower() == "yes":
                print(summarize_chat(session))
        
        clear_chat_option = input("Do you want to clear the previous chat and start a new session? (yes/no): ")
        if clear_chat_option.lower() == 'yes':
            session.clear_chat_history()
            print("Starting a new session.")

        # Asking the questions in a loop
        for question in questions:
            user_input = ask_patient_question(question)
            store_chat_message(session, "User", user_input)

        # Generating medical response based on inputs
        response_suggestions = generate_medical_response(session.specialty, continuity_prompt, session)
        store_chat_message(session, "Bot", response_suggestions)  # Save bot response
        print("Bot: ", response_suggestions)

        # Looping for continuing or dumping the chat
        while True:
            options = ["1. Continue the conversation", "2. Dump the old chat and start a new session"]
            print("\n".join(options))
            choice = input("Enter the number corresponding to your choice: ")
            if choice == "1":
                user_input = ask_patient_question(continuity_prompt)
                store_chat_message(session, "User", user_input)
                response_suggestions = generate_medical_response(session.specialty, continuity_prompt, session)
                store_chat_message(session, "Bot", response_suggestions)  # Save bot response
                print("Bot: ", response_suggestions)
            elif choice == "2":
                session.clear_chat_history()
                print("Starting a new session.")

                # Asking the questions in a loop for the new session
                for question in questions:
                    user_input = ask_patient_question(question)
                    store_chat_message(session, "User", user_input)

                # Generating medical response based on inputs for the new session
                response_suggestions = generate_medical_response(session.specialty, continuity_prompt, session)
                store_chat_message(session, "Bot", response_suggestions)  # Save bot response
                print("Bot: ", response_suggestions)
    else:
        print("Session could not be started.")

def summarize_chat(session):
    if not session.chat_history:
        return "No chat history available for summarization."

    user_messages = []
    bot_messages = []
    for message in session.chat_history:
        role, content = message.split(": ", 1)
        if role.strip() == "User":
            user_messages.append(content.strip())
        elif role.strip() == "Bot":
            bot_messages.append(content.strip())

    user_summary = "\n".join(user_messages)
    bot_summary = "\n".join(bot_messages)

    summary = f"User's messages:\n{user_summary}\n\nBot's messages:\n{bot_summary}\n\nBased on our conversation, it seems like you are experiencing symptoms related to anxiety. You mentioned feeling worried constantly and having panic attacks, which are often triggered by social situations and uncertainty. These symptoms have been affecting you for several years, leading to avoidance of social gatherings and difficulty concentrating.\n\nIn response to your concerns, we discussed strategies such as practicing relaxation techniques, engaging in cognitive-behavioral therapy (CBT), considering medications like SSRIs or benzodiazepines, and exploring resources like support groups, yoga, and mindfulness meditation. We also recommended journal articles related to anxiety disorders for further reading.\n\nLet's continue working together to implement these strategies and monitor your progress. Your well-being is our priority."

    return summary




session = start_session()
chat_interaction(session)