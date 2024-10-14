import json
import random
import nltk
from nltk.stem import WordNetLemmatizer

# Load the intents file
lemmatizer = WordNetLemmatizer()
nltk.download('punkt')
nltk.download('wordnet')

# Load intents JSON
with open('intents.json') as file:
    data = json.load(file)


# Preprocessing: Tokenizing and Lemmatizing
def tokenize_sentence(sentence):
    return nltk.word_tokenize(sentence)


def lemmatize_word(word):
    return lemmatizer.lemmatize(word.lower())


# Matching user input with intents
def get_intent(user_input):
    for intent in data['intents']:
        for pattern in intent['patterns']:
            tokenized_pattern = tokenize_sentence(pattern)
            tokenized_input = tokenize_sentence(user_input)

            # Simple matching using word comparison
            if set(lemmatize_word(word) for word in tokenized_pattern) == set(
                    lemmatize_word(word) for word in tokenized_input):
                return intent['tag']
    return None


# Response based on intent
def get_response(intent_tag):
    for intent in data['intents']:
        if intent['tag'] == intent_tag:
            return random.choice(intent['responses'])
    return "I'm sorry, I don't understand."


# Chatbot interaction
def chatbot_response(user_input):
    intent = get_intent(user_input)
    if intent:
        return get_response(intent)
    else:
        return "Sorry, I don't understand that."


# Simple loop for chatbot conversation
if __name__ == "__main__":
    print("Chatbot is ready! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        print("Bot:", chatbot_response(user_input))


