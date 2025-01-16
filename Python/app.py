from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Load Bhagavad Gita dataset
file_path = 'Bhagwad_Gita.xlsx'
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found. Please ensure it exists in the working directory.")
    exit()

# Initialize sentiment analysis components
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Emotion-to-verse mapping
emotion_verse_map = {
    # Mapping truncated for brevity; use the full mapping from the input code
}

# Initialize chatbot model
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input_text = msg.lower()

    # Check for emotions and suggest verses if detected
    emotion = map_emotion_to_text(input_text)
    if emotion:
        suggested_verse = suggest_verse(emotion, df)
        response = {
            "Chatbot": "I sense some emotion in your input. Here's a relevant verse from the Bhagavad Gita:",
            "Emotion": emotion.capitalize(),
            "Chapter": suggested_verse["Chapter"],
            "Verse": suggested_verse["Verse"],
            "Shloka": suggested_verse["Shloka"],
            "Transliteration": suggested_verse["Transliteration"],
            "Hindi Meaning": suggested_verse["HinMeaning"],
            "English Meaning": suggested_verse["EngMeaning"]
        }
        return jsonify(response)

    # Fall back to chatbot if no emotion detected
    bot_response = get_Chat_response(input_text)
    return jsonify({"Chatbot": bot_response})

def get_Chat_response(text):
    """Generate a chatbot response."""
    new_user_input_ids = tokenizer.encode(str(text) + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = new_user_input_ids
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    bot_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return bot_response

def analyze_sentiment(text):
    """Analyze the sentiment of the input text."""
    sentiment = sia.polarity_scores(text)
    if sentiment['compound'] >= 0.05:
        return 'positive'
    elif sentiment['compound'] <= -0.05:
        return 'negative'
    else:
        return 'neutral'

def map_emotion_to_text(text):
    """Map user input to an emotion based on keywords."""
    keyword_map = {
        "anger": ["angry", "rage", "furious"],
        "depression": ["sad", "depressed", "down"],
        "discriminated": ["unfair", "biased"],
        "greed": ["greedy", "selfish"],
        "laziness": ["lazy", "procrastinate"],
        "practicing forgiveness": ["forgive", "peaceful"],
        "pride": ["proud", "arrogant"],
        "confusion": ["confused", "lost"],
        "dealing with envy": ["envy", "jealous"],
        "fear": ["scared", "afraid", "fear"],
        "loneliness": ["lonely", "alone"],
        "death of a loved one": ["grief", "loss", "death"],
        "demotivated": ["unmotivated", "demotivated"],
        "feeling sinful": ["guilt", "sinful"],
        "seeking peace": ["calm", "tranquil"],
        "losing hope": ["hopeless", "despair"],
        "temptation": ["tempted", "desire"],
        "forgetfulness": ["forgetful", "forget"],
        "lust": ["lustful", "desire"],
        "uncontrolled mind": ["distracted", "unfocused"]
    }
    for emotion, keywords in keyword_map.items():
        if any(word in text for word in keywords):
            return emotion
    return None

def suggest_verse(emotion, df):
    """Suggest a verse based on the emotion."""
    if emotion and emotion in emotion_verse_map:
        verse_ids = emotion_verse_map[emotion]
        matches = df[df['ID'].isin(verse_ids)]
        if not matches.empty:
            return matches.sample().iloc[0]
    # Default fallback if no specific match is found
    return df.sample().iloc[0]

if __name__ == '__main__':
    app.run(debug=True)
