import speech_recognition as sr
import pyttsx3
import webbrowser
import tkinter as tk
from tkinter import scrolledtext, messagebox
import time  # For adding delays

# Initialize the pyttsx3 engine for text-to-speech
engine = pyttsx3.init()

# Set speech properties (optional)
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume level (0.0 to 2.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # [0] is male, [1] is female

# Initialize recognizer for speech recognition
recognizer = sr.Recognizer()

# Function to process speech input and recognize commands
def listen_to_user():
    global chat_log
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        try:
            engine.say("Listening... Please speak now.")
            engine.runAndWait()
            time.sleep(0.5)  # Add a slight delay to allow TTS to finish before listening

            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            query = recognizer.recognize_google(audio, language="en-in")

            # Display the recognized text in the GUI
            chat_log.insert(tk.END, "You: " + query + "\n")
            process_command(query)

        except sr.UnknownValueError:
            engine.say("Sorry, I didn't catch that.")
            engine.runAndWait()
            chat_log.insert(tk.END, "Sorry, I didn't understand.\n")

        except sr.RequestError as e:
            engine.say("Could not request results. Check your internet connection.")
            engine.runAndWait()
            chat_log.insert(tk.END, "Error: Could not connect.\n")

        except sr.WaitTimeoutError:
            engine.say("Listening timed out.")
            engine.runAndWait()
            chat_log.insert(tk.END, "Error: Listening timed out.\n")

# Function to process recognized commands
def process_command(query):
    global chat_log
    query = query.lower()

    if "open youtube" in query:
        webbrowser.open("https://youtube.com")
        engine.say("Opening YouTube")
        chat_log.insert(tk.END, "CONVO AI: Opening YouTube\n")
    elif "open google" in query:
        webbrowser.open("https://google.com")
        engine.say("Opening Google")
        chat_log.insert(tk.END, "CONVO AI: Opening Google\n")
    else:
        # For any other text or queries
        chat_log.insert(tk.END, "CONVO AI: I don't understand that command.\n")
        engine.say("I don't understand that command.")

    engine.runAndWait()

# Function to handle text input from the user
def send_message():
    global chat_log, user_input
    user_message = user_input.get()
    chat_log.insert(tk.END, "You: " + user_message + "\n")
    user_input.delete(0, tk.END)
    process_command(user_message)

# Function to create the GUI for the chatbot
def create_chatbot_app():
    global chat_log, user_input

    # Customize the main application window
app = tk.Tk()
app.title("CONVO AI Chatbot")
app.geometry("500x600")
app.config(bg="#02333B")  # Light gray background for the app

# Customize the scrollable chat window
chat_log = scrolledtext.ScrolledText(app, wrap=tk.WORD, height=20, width=50, state='normal',
                                     font=("Courier", 10), bg="#ffffff", fg="#333333", padx=10, pady=10)
chat_log.pack(pady=10)

# Customize the entry field for user input
user_input = tk.Entry(app, width=50, font=("Arial", 12), bg="#e6e6e6", fg="#000000", borderwidth=3, relief="groove")
user_input.pack(pady=10)

# Create customized buttons for sending text and for voice input
send_button = tk.Button(app, text="Send Text", command=send_message, 
                        bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), 
                        padx=10, pady=5, borderwidth=2, relief="raised")
send_button.pack(pady=5)

voice_button = tk.Button(app, text="Speak", command=listen_to_user, 
                         bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"), 
                         padx=10, pady=5, borderwidth=2, relief="raised")
voice_button.pack(pady=5)

# Run the application loop
app.mainloop()

# Start the chatbot application
create_chatbot_app()

    


    