import os
from google import genai
from datetime import datetime

# Get API key from environment variable
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable")

client = genai.Client(api_key=api_key)
doctor = genai.Client(api_key="AIzaSyCVj0TbgZy8LMA6OXvFJZqwSdvQOgebWpk")

print("Welcome! I'm your medical assistant. Type 'done', 'exit', or 'quit' when you have no more questions.")
print("How can I help you today?")

# Initialize conversation history
conversation_history = []
diagnosis_boolets = []
symptoms_boolets = []

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

while True:
    # Get user input
    user_input = input("\nYou: ").strip().lower()
    
    # Log user input with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('logs/user_input.log', 'a', encoding='utf-8') as log_file:
        log_file.write(f"[{timestamp}] User: {user_input}\n")
    
    # Check for exit conditions
    if user_input in ['done', 'exit', 'quit', 'no more', 'that\'s all']:
        print("\nThank you for using our medical assistant. Please remember to consult with a healthcare professional for proper medical advice.")
        break
    
    # Add explanation to the user's input
    prompt = f"""Please analyze and respond to the following user input. 
The user should be asking about symptoms and diagnosis. 
Please provide a relevant follow up question to the user's input if needed.
If the user is asking about unrelated topics, please kindly ask them to contact a professional for advice.
Notice that you are a medical assistant that gathers information about a patient symptoms and should act as one.
we want to keep the conversation focused so each time ask one question and spare the preview and prolog for later.

if you have more then 20 symptoms, please ask the user to contact a professional for advice.
if you see that there is no more symptoms to collect, please return "no more symptoms to collect".

prevoius symptoms collected: {symptoms_boolets}
User's question/symptoms: {user_input}"""

    # Add conversation history to context if available
    if conversation_history:
        history_context = "\nPrevious conversation:\n" + "\n".join(conversation_history[-3:])  # Keep last 3 exchanges
        prompt = history_context + "\n\n" + prompt

    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=prompt
    )
    doctor_prompt = f"""
    You are a medical assistant that gathers information about a patient symptoms and should act as one.
    You get a list of symptoms that grow over time from a patient.
    Please provide a relevant bollets for the siptoms, the bollets should be in the form of a string when each symptom is a new line.
    avoid adding additional information to the bollets, just the symptoms and the bollets.
    e.g (dont make a title for the bollets, just the symptoms and details if needed)
    - Fever - 38C - 2 days
    - Cough - 1 day
    - Sore throat - aches when swallowing - 1 day
    if the symptoms are not related to the patient, or the input is unrelated to the patient, or the input is not clear, dont return anything.
    if the patient asks about the diagnosis, please explain that you are not a doctor ai and the first diagnosis is based on the symptoms you collected.

    if you see that there is no more symptoms to collect, please return "no more symptoms to collect".
    
    Symptoms:   q: {response}
                a: {user_input}
    """
    
    doctor_response = doctor.models.generate_content(
        model="gemini-2.0-flash",
        contents=doctor_prompt
    )

    # Store the exchange in history
    conversation_history.append(f"You: {user_input}")
    conversation_history.append(f"Assistant: {response.text}")
    symptoms_boolets.append(doctor_response.text)
    print("\nAssistant:", response.text)
    if response.text == "no more symptoms to collect" or doctor_response.text == "no more symptoms to collect" or doctor_response.text == "no more symptoms to collect.":
        break

print(symptoms_boolets)