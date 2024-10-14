import speech_recognition as sr
import pyttsx3
import datetime
import random
import os
import webbrowser

# Initialize the pyttsx3 engine for text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Use female voice


# Initialize recognizer for speech recognition
recognizer = sr.Recognizer()

# Global flags
mode = "speech"  # Can be "text" or "speech" mode
listening = True  # Controls whether the bot is actively listening

# Function to make the chatbot speak
def speak(text):
    """Text-to-Speech function"""
    engine.say(text)
    engine.runAndWait()

# Function to listen for voice commands
def listen_command():
    global recognizer
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for ambient noise
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)
            command = recognizer.recognize_google(audio, language="en-in").lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I could not understand that.")
            return None
        except sr.RequestError:
            speak("There was an error with the speech recognition service.")
            return None

# Function to process basic commands
def process_command(command):
    """Processes various user commands"""
    if 'time' in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
    elif 'date' in command:
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {current_date}.")
    elif 'joke' in command:
        joke = random.choice([
            "Why did the computer go to the doctor? Because it had a virus.",
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "Why was the math book sad? It had too many problems."
        ])
        speak(joke)
    elif 'open youtube' in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif 'open google' in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif 'exit' in command or 'quit' in command:
        speak("Goodbye!")
        return False  # Exit the conversation loop
    return True  # Continue listening after task is done

# Main function to handle continuous interaction
def main():
    global mode, listening
    speak("Hello, I am CONVO AI. How can I assist you today?")

    while True:
        if listening:
            if mode == "speech":
                # Listen for voice command
                command = listen_command()
            else:
                # Accept text input
                command = input("Type your command: ").lower()

            if command:
                # Mode switching commands
                if 'switch to text' in command:
                    mode = "text"
                    speak("Switching to text mode.")
                elif 'switch to speech' in command:
                    mode = "speech"
                    speak("Switching to speech mode.")
                elif 'stop listening' in command:
                    speak("I will stop listening now. Say 'resume listening' to wake me up.")
                    listening = False
                elif 'resume listening' in command:
                    speak("I am listening again.")
                    listening = True
                elif 'exit' in command or 'quit' in command:
                    speak("Goodbye!")
                    break
                else:
                    # Process the command normally
                    task_completed = process_command(command)
                    if not task_completed:
                        break  # Exit if task completed with exit command
        else:
            # Wait for the user to type "resume listening"
            command = input("Type 'resume listening' to wake me up: ").lower()
            if 'resume listening' in command:
                speak("I am listening again.")
                listening = True

if __name__ == "__main__":
    main()
    import requests

    # Google API setup: Replace these with your actual API key and search engine ID
    API_KEY = "YOUR_GOOGLE_API_KEY"
    SEARCH_ENGINE_ID = "YOUR_SEARCH_ENGINE_ID"


    def google_search(query):
        """Search Google using the Custom Search API."""
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}"
        response = requests.get(url)
        results = response.json()

        # Extract search results from the response
        if "items" in results:
            search_results = results['items']
            # Return titles, snippets, and links of the top results
            return [(item['title'], item['snippet'], item['link']) for item in search_results]
        else:
            return "No results found."
def process_command(command):
    """Processes various user commands."""
    if 'search' in command:
        # Extract the search query from the command
        query = command.replace('search', '').strip()
        speak(f"Searching Google for {query}")
        results = google_search(query)

        # Read out the top 3 results
        if results != "No results found.":
            for title, snippet, link in results[:3]:  # Limit to top 3 results
                speak(f"Result: {title}. {snippet}. More info at {link}")
        else:
            speak("Sorry, I couldn't find anything.")
    # Other commands...
def speak(text):
    """Text-to-Speech function."""
    engine.say(text)
    engine.runAndWait()
    import requests
    from bs4 import BeautifulSoup

    def scrape_webpage(url):
        """Scrapes general information from a given webpage."""
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract Titles (Headlines)
        titles = [title.get_text() for title in soup.find_all('h1')] + \
                 [title.get_text() for title in soup.find_all('h2')] + \
                 [title.get_text() for title in soup.find_all('h3')]

        # Extract Paragraphs
        paragraphs = [para.get_text() for para in soup.find_all('p')]

        # Extract Links
        links = [a['href'] for a in soup.find_all('a', href=True)]

        # Extract Images
        images = [img['src'] for img in soup.find_all('img', src=True)]

        # Extract Meta Information (Description, Keywords)
        description = soup.find('meta', attrs={'name': 'description'})
        keywords = soup.find('meta', attrs={'name': 'keywords'})

        # Store and return all scraped data
        scraped_data = {
            "titles": titles,
            "paragraphs": paragraphs,
            "links": links,
            "images": images,
            "description": description['content'] if description else "No description",
            "keywords": keywords['content'] if keywords else "No keywords"
        }

        return scraped_data


def process_command(command):
    if 'fetch information' in command:
        # Extract the URL from the command
        url = command.replace('fetch information from', '').strip()
        speak(f"Fetching information from {url}")

        # Scrape data from the webpage
        scraped_data = scrape_webpage(url)

        # Read out the first few titles and paragraphs
        for title in scraped_data['titles'][:3]:
            speak(f"Title: {title}")
        for para in scraped_data['paragraphs'][:3]:
            speak(f"Paragraph: {para}")
    # Handle other commands like time, joke, etc.


