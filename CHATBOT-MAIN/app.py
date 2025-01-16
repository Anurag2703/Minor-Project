from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import nltk

# Initialize sentiment analysis components
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Load Bhagavad Gita dataset
file_path = 'Bhagwad_Gita.xlsx'
df = pd.read_excel(file_path)

# Initialize chatbot model
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Define emotion keywords
emotion_keywords = {"sad", "happy", "angry", "joyful", "upset", "depressed", "excited", "fearful"}

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input_text = msg.lower()
    return get_Chat_response(input_text)

def analyze_sentiment(text):
    """Analyze the sentiment of the user's message."""
    sentiment = sia.polarity_scores(text)
    if sentiment['compound'] >= 0.05:
        return 'positive'
    elif sentiment['compound'] <= -0.05:
        return 'negative'
    else:
        return 'neutral'

def suggest_verse(sentiment):
    """Suggest a Bhagavad Gita verse based on the sentiment."""
    if sentiment == 'positive':
        happy_verses = df[df['EngMeaning'].str.contains('joy|happy|elevate', case=False, na=False)]
        if not happy_verses.empty:
            verse = happy_verses.sample().iloc[0]
        else:
            verse = df.sample().iloc[0]
    else:
        verse = df.sample().iloc[0]
    return {
        "ID": verse["ID"],
        "Chapter": verse["Chapter"],
        "Verse": verse["Verse"],
        "Shloka": verse["Shloka"],
        "Transliteration": verse["Transliteration"],
        "Hindi Meaning": verse["HinMeaning"],
        "English Meaning": verse["EngMeaning"],
        "Word Meaning": verse["WordMeaning"],
    }

def get_Chat_response(text):
    """
    Generate a chatbot response. Trigger sentiment analysis and Bhagavad Gita verse suggestion
    only if the text contains emotion-related keywords.
    """
    # Check if text contains emotion keywords
    if any(word in text for word in emotion_keywords):
        # Analyze sentiment
        sentiment = analyze_sentiment(text)
        # Suggest a verse based on sentiment
        verse = suggest_verse(sentiment)
        return (
            f"It seems you're feeling {sentiment}. Here's something from the Bhagavad Gita to reflect upon:\n\n"
            f"Chapter: {verse['Chapter']}, Verse: {verse['Verse']}\n"
            f"Shloka: {verse['Shloka']}\n"
            f"Translation: {verse['Transliteration']}\n"
            f"English Meaning: {verse['English Meaning']}\n"
        )
    else:
        # Generate a normal chatbot response
        new_user_input_ids = tokenizer.encode(str(text) + tokenizer.eos_token, return_tensors='pt')
        bot_input_ids = new_user_input_ids
        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        bot_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        return f"{bot_response}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
