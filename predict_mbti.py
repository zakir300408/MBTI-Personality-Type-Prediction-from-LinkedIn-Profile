import os
import fitz  # PyMuPDF
import requests
import json

# OpenRouter API key
OPENROUTER_API_KEY = "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"  

# OpenRouter API base URL
base_url = "https://openrouter.ai/api/v1/chat/completions"

# Models
model_name_primary = "meta-llama/llama-3.2-3b-instruct:free"
model_name_supervisor = "meta-llama/llama-3.2-3b-instruct:free"


def extract_text_from_pdf(pdf_path):
    """
    Extract text from the PDF file
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text


def clean_text(text):
    """
    Clean the extracted text by removing new lines and extra spaces
    """
    cleaned_text = text.replace("\n", " ").strip()
    return cleaned_text


def get_personality_prediction(text, model_name, temperature=0.7, max_tokens=1000):
    """
    Use the primary model to predict the MBTI personality type
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system",
             "content": "You are an assistant that predicts the MBTI personality type based on written descriptions. Analyze the text and provide the most likely MBTI type."},
            {"role": "user", "content": f"Please predict the MBTI personality type for the following text: {text}"}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    response = requests.post(base_url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"


def get_supervisor_feedback(prediction, text):
    """
    Use the supervisor model to evaluate the MBTI prediction and provide confidence in the result
    """
    possible_types = extract_possible_types(prediction)
    relevant_context = text[:1000]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_name_supervisor,
        "messages": [
            {"role": "system",
             "content": "You are an expert psychologist and MBTI specialist. Your task is to evaluate the confidence in the predicted MBTI types based on the context provided. "
                        "Only assess the top predicted types and provide a confidence percentage for each, based on the context. Give confidence levels in this format: "
                        "'Most likely INTJ, 75% confident. INTP, 25% confident.'"},
            {"role": "user",
             "content": f"Here is the predicted MBTI type(s): {possible_types}. The relevant context is: {relevant_context}. Please evaluate the confidence levels for the predicted types."}
        ],
        "temperature": 0.5,
        "max_tokens": 1000
    }

    response = requests.post(base_url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"


def extract_possible_types(prediction):
    """
    Extract possible MBTI types from the initial prediction output
    """
    types = []
    if "INTJ" in prediction:
        types.append("INTJ")
    if "INTP" in prediction:
        types.append("INTP")
    if "ENFP" in prediction:
        types.append("ENFP")
    if "ENTJ" in prediction:
        types.append("ENTJ")

    return ", ".join(types[:3])


def get_final_prediction(pdf_path):
    """
    Extract text from the PDF, get the initial prediction, and verify it using the supervisor model
    """
    raw_text = extract_text_from_pdf(pdf_path)
    cleaned_text = clean_text(raw_text)

    prediction = get_personality_prediction(cleaned_text, model_name_primary)
    print(f"Initial MBTI Prediction: {prediction}")

    feedback = get_supervisor_feedback(prediction, cleaned_text)
    print(f"Supervisor Feedback: {feedback}")

    confidence_levels = parse_confidence(feedback)

    print(f"Final Prediction: {confidence_levels['final_prediction']}")
    print("Confidence Distribution:")
    for personality, confidence in confidence_levels['distribution'].items():
        print(f"{personality}: {confidence}%")


def parse_confidence(feedback):
    """
    Parse the supervisor's feedback and extract the MBTI type with confidence levels
    """
    confidence_levels = {
        'distribution': {},
        'final_prediction': ''
    }

    if "Most likely" in feedback and "%" in feedback:
        parts = feedback.split(".")
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


# Replace with the path to your PDF file
pdf_path = "Profile.pdf"
get_final_prediction(pdf_path)
