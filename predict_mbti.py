import os
import fitz  # PyMuPDF
import requests
import json
import re

#add my proxy to the environment if needed or you may comment it
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

OPEN_ROUTER = os.getenv('OPEN_ROUTER')

# OpenRouter API base URL
base_url = "https://openrouter.ai/api/v1/chat/completions"

# Models
model_name_primary = "meta-llama/llama-3.2-3b-instruct:free"
model_name_supervisor = "meta-llama/llama-3.2-3b-instruct:free"
model_name_psychologist = "nousresearch/hermes-3-llama-3.1-405b:free"
model_name_industry_specialist = "nousresearch/hermes-3-llama-3.1-405b:free"

# All 16 MBTI Types
MBTI_TYPES = [
    "INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"
]

def extract_text_from_pdf(pdf_path):
    #extract text from the pdf file
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text

def clean_text(text):
    #clean the extracted text from the pdf
    text = re.sub(r'[•\-|<>]', ' ', text)  # remove special characters
    text = re.sub(r'\s+', ' ', text)  # normalize whitespace
    text = re.sub(r'&\w+;', ' ', text)  # remove HTML-like artifacts
    text = re.sub(r'Page \d+ of \d+', ' ', text, flags=re.IGNORECASE)  # strip headers/footers

    #filter by keywords
    keywords = ["experience", "skills", "education", "projects", "certifications"]
    sections = [line for line in text.splitlines() if any(k in line.lower() for k in keywords)]
    text = ' '.join(sections).strip()
    return text

def get_personality_prediction(text, model_name, temperature=0.7, max_tokens=1000):
    #get mbti prediction using the api
    headers = {
        "Authorization": f"Bearer {OPEN_ROUTER}",
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
    return response.json()['choices'][0]['message']['content'] if response.status_code == 200 else f"Error: {response.status_code} - {response.text}"

def get_supervisor_feedback(prediction, text):
    #evaluate mbti prediction confidence
    headers = {
        "Authorization": f"Bearer {OPEN_ROUTER}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_name_supervisor,
        "messages": [
            {"role": "system",
             "content": "You are an expert psychologist and MBTI specialist. Your task is to evaluate the confidence in the predicted MBTI types based on the context provided. Give confidence levels in this format: 'Most likely INTJ, 75% confident. INTP, 25% confident.'"},
            {"role": "user",
             "content": f"Here is the predicted MBTI type(s): {prediction}. The relevant context is: {text[:1000]}. Please evaluate the confidence levels for the predicted types."}
        ],
        "temperature": 0.5,
        "max_tokens": 1000
    }
    response = requests.post(base_url, headers=headers, data=json.dumps(payload))
    return response.json()['choices'][0]['message']['content'] if response.status_code == 200 else f"Error: {response.status_code} - {response.text}"

def psychologist_analysis(text, personality_prediction):
    #analyze psychometric traits based on prediction
    headers = {
        "Authorization": f"Bearer {OPEN_ROUTER}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_name_psychologist,
        "messages": [
            {"role": "system",
             "content": "You are a psychologist specializing in psychometric analysis. Analyze traits like creativity, leadership, and risk tolerance based on the MBTI prediction and text provided."},
            {"role": "user", "content": f"Personality: {personality_prediction}. Analyze the following text: {text}"}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    response = requests.post(base_url, headers=headers, data=json.dumps(payload))
    return response.json()['choices'][0]['message']['content'] if response.status_code == 200 else f"Error: {response.status_code} - {response.text}"

def map_personality_to_industry(personality_prediction, psychometric_insights):
    #map personality to industry roles
    headers = {
        "Authorization": f"Bearer {OPEN_ROUTER}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_name_industry_specialist,
        "messages": [
            {"role": "system",
             "content": "You are an industry specialist. Your task is to align personality traits and psychometric insights with job roles in the candidate's most recent industry."},
            {"role": "user",
             "content": f"Personality: {personality_prediction}. Insights: {psychometric_insights}. Suggest roles in the most recent industry of the candidate."}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    response = requests.post(base_url, headers=headers, data=json.dumps(payload))
    return response.json()['choices'][0]['message']['content'] if response.status_code == 200 else f"Error: {response.status_code} - {response.text}"

def multi_agent_communication(pdf_path):
    #coordinate agents to produce results
    raw_text = extract_text_from_pdf(pdf_path)
    cleaned_text = clean_text(raw_text)
    print(f"Cleaned Text: {cleaned_text[:500]}...")  # preview text for debugging

    primary_prediction = get_personality_prediction(cleaned_text, model_name_primary)
    print(f"Primary Prediction: {primary_prediction}")

    supervisor_feedback = get_supervisor_feedback(primary_prediction, cleaned_text)
    print(f"Supervisor Feedback: {supervisor_feedback}")

    psychometric_insights = psychologist_analysis(cleaned_text, primary_prediction)
    print(f"Psychometric Insights: {psychometric_insights}")

    industry_analysis = map_personality_to_industry(primary_prediction, psychometric_insights)
    print(f"Industry Analysis: {industry_analysis}")

    return {
        "primary_prediction": primary_prediction,
        "supervisor_feedback": supervisor_feedback,
        "psychometric_insights": psychometric_insights,
        "industry_analysis": industry_analysis
    }

# Replace with the path to your LinkedIn PDF file
pdf_path = "Profile.pdf"
results = multi_agent_communication(pdf_path)

print("\nFinal Results:")
print(f"Primary Prediction: {results['primary_prediction']}")
print(f"Supervisor Feedback: {results['supervisor_feedback']}")
print(f"Psychometric Insights: {results['psychometric_insights']}")
print(f"Industry Analysis: {results['industry_analysis']}")
