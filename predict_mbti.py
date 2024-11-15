import os
import fitz  # PyMuPDF
import requests
import json

# OpenRouter API key
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

# OpenRouter API base URL
base_url = "https://openrouter.ai/api/v1/chat/completions"

# Models
model_name_primary = "meta-llama/llama-3.2-3b-instruct:free"
model_name_supervisor = "meta-llama/llama-3.2-3b-instruct:free"
model_name_psychologist = "meta-llama/llama-3.2-3b-instruct:free"  # Same model for simplicity; can use a different one for this task

# All 16 MBTI Types
MBTI_TYPES = [
    "INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"
]

def extract_text_from_pdf(pdf_path):
    """ Extract text from the PDF file """
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text

def clean_text(text):
    """ Clean the extracted text by removing new lines and extra spaces """
    return text.replace("\n", " ").strip()

def get_personality_prediction(text, model_name, temperature=0.7, max_tokens=1000):
    """ Get the MBTI personality prediction """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are an assistant that predicts the MBTI personality type based on written descriptions. Analyze the text and provide the most likely MBTI type."},
            {"role": "user", "content": f"Please predict the MBTI personality type for the following text: {text}"}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    response = requests.post(base_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

def get_supervisor_feedback(prediction, text):
    """ Evaluate the MBTI prediction and provide confidence """
    relevant_context = text[:1000]  # Taking the first 1000 chars for context

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_name_supervisor,
        "messages": [
            {"role": "system", "content": "You are an expert psychologist and MBTI specialist. Your task is to evaluate the confidence in the predicted MBTI types based on the context provided. Give confidence levels in this format: 'Most likely INTJ, 75% confident. INTP, 25% confident.'"},
            {"role": "user", "content": f"Here is the predicted MBTI type(s): {prediction}. The relevant context is: {relevant_context}. Please evaluate the confidence levels for the predicted types."}
        ],
        "temperature": 0.5,
        "max_tokens": 1000
    }

    response = requests.post(base_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

def parse_confidence(supervisor_feedback):
    """ Parse supervisor feedback to extract confidence levels """
    confidence_levels = {'distribution': {}, 'final_prediction': ''}
    if "Most likely" in supervisor_feedback and "%" in supervisor_feedback:
        parts = supervisor_feedback.split(".")
        for part in parts:
            part = part.strip()
            if "Most likely" in part:
                final_type = part.split(",")[0].replace("Most likely", "").strip()
                confidence = part.split(",")[1].replace("% confident", "").strip()
                confidence_levels['final_prediction'] = f"{final_type}-{confidence}%"
            elif "%" in part:
                confidence_str = part.split(",")
                if len(confidence_str) > 1:
                    personality = confidence_str[0].strip()
                    confidence = confidence_str[1].replace("% confident", "").strip()
                    confidence_levels['distribution'][personality] = confidence
    return confidence_levels

def get_final_prediction(pdf_path):
    """ Extract text, get prediction, and calculate final confidence distribution """
    raw_text = extract_text_from_pdf(pdf_path)
    cleaned_text = clean_text(raw_text)

    # Get initial personality prediction
    primary_prediction = get_personality_prediction(cleaned_text, model_name_primary)
    print(f"Initial MBTI Prediction: {primary_prediction}")

    # Get supervisor feedback and confidence distribution
    supervisor_feedback = get_supervisor_feedback(primary_prediction, cleaned_text)
    print(f"Supervisor Feedback: {supervisor_feedback}")

    # Parse supervisor feedback
    confidence_levels = parse_confidence(supervisor_feedback)

    print(f"Final Prediction: {confidence_levels['final_prediction']}")
    print("Confidence Distribution:")
    for personality, confidence in confidence_levels['distribution'].items():
        print(f"{personality}: {confidence}%")

# Replace with the path to your PDF file
pdf_path = "Profile.pdf"
get_final_prediction(pdf_path)
