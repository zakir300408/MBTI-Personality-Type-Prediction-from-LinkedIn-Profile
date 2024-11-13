# MBTI Personality Type Prediction from LinkedIn Profile

This project uses machine learning models to predict a person's MBTI (Myers-Briggs Type Indicator) personality type based on text data. You can provide a LinkedIn profile or any other written content. The system uses two models:

- A **primary model** to predict the MBTI type based on the provided text.
- A **supervisor model** that checks the prediction and provides feedback on how confident the system is in its prediction.

## Requirements

### 1. Python 3.8+
You need Python version 3.8 or higher installed on your machine.

### 2. Required Libraries
Install the necessary libraries using `pip`:

```bash
pip install openai pymupdf
```


### 3. OpenAI API Key
You will need an OpenAI API key to use the models for both predictions and feedback. Here's how to get and set it up:

#### Steps to Get the OpenAI API Key:
1. **Create an OpenAI Account**:  
   Go to [OpenAI](https://platform.openai.com) and create an account if you don't have one already.

2. **Generate an API Key**:  
   After logging into OpenAI, go to the **API keys** section in your account dashboard. Generate a new secret key (or use an existing one) and copy it.

#### Set Up the API Key:
Once you have your API key, you need to configure it in your environment. You can set the key as an environment variable in your terminal:

- **On macOS/Linux (using bash)**:
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

- **On Windows (using PowerShell)**:
```bash
- $env:OPENAI_API_KEY="your-openai-api-key-here"
```

Alternatively, you can hardcode the API key directly in the script, but storing it as an environment variable is more secure.

## How to Use the System

### Step 1: Download Your LinkedIn Profile
To use the system with your LinkedIn profile, download it in PDF format:

1. Go to your LinkedIn profile.
2. Click **"More..."** (next to your profile picture).
3. Select **"Save to PDF"**.
4. The PDF will be saved to your computer.
5. Save the PDF to your local machine.

### Step 2: Place the PDF in Your Working Directory
Move or copy the downloaded LinkedIn PDF into the same folder where the Python script is located, or note its file path if you plan to use a different location.

### Step 3: Run the Script
Once the PDF is in the folder, you can now run the script to get the MBTI prediction.

1. Open a terminal or command prompt.
2. Go to the folder where the script is located.
3. Run the command:

```bash
python predict_mbti.py
```

The script will:

- Extract text from the LinkedIn profile PDF.
- Send the text to the primary model to get an MBTI prediction.
- Pass the prediction to the supervisor model for feedback and confidence levels.

### Step 4: View the Results
Once the script finishes, the output will include:

- **Initial MBTI Prediction** based on the provided text.
- **Supervisor Feedback**, showing the confidence level for the most likely MBTI types.
- **Final MBTI Prediction**, with confidence scores for each possible type.

Example output:

```yaml
Initial MBTI Prediction: INTJ
Supervisor Feedback: Most likely INTJ, 75% confident. INTP, 25% confident.
Final Prediction: INTJ-75%
Confidence Distribution:
  INTJ: 75%
  INTP: 25%
```

