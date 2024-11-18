# MBTI Personality Type Prediction and Analysis from LinkedIn Profile

this project predicts and analyzes a person's MBTI (Myers-Briggs Type Indicator) personality type based on written content, such as LinkedIn profiles or other documents. it uses multiple AI models working collaboratively to deliver a comprehensive report, including personality prediction, confidence analysis, psychometric insights, and industry-specific career suggestions.

## Overview of Agents

1. **Primary Agent**  
   - predicts the MBTI personality type based on the provided text.

2. **Supervisor Agent**  
   - evaluates the primary prediction and provides confidence levels for each possible MBTI type.

3. **Psychologist Agent**  
   - performs psychometric analysis, assessing traits like creativity, leadership, and risk tolerance.

4. **Industry Specialist Agent**  
   - maps personality traits and psychometric insights to career roles in the candidate’s industry.

## Features

- **MBTI Prediction**: predicts the MBTI type (e.g., INTJ, ENFP) from text.
- **Confidence Levels**: evaluates how confident the system is in the prediction.
- **Psychometric Insights**: analyzes key traits such as problem-solving skills, teamwork, or decision-making.
- **Career Mapping**: suggests potential job roles in line with the user’s personality and skills.

## Requirements

### 1. Python 3.8+
ensure you have Python version 3.8 or later installed.

### 2. openrouter API Key
you’ll need an openrouter API key to use the models. follow these steps to get and configure the API key:

#### Steps to Get the openrouter API Key:
1. **create an openrouter account**:  
   visit [openrouter](https://openrouter.ai/) and sign up if you don’t already have an account.

2. **generate an API key**:  
   go to the **API keys** section of your account dashboard, generate a new key, and copy it.

#### Configure the API Key:
set the API key as an environment variable:

- **On macOS/Linux**:
  `export OPEN_ROUTER="your-openrouter-api-key-here"`

- **On Windows**:
  `$env:OPEN_ROUTER="your-openrouter-api-key-here"`

alternatively, hardcode it directly in the script, though this is less secure.

## How to Use the System

### Step 1: Prepare Your Profile
download your LinkedIn profile in PDF format:

1. go to your LinkedIn profile.
2. click **"More..."** next to your profile picture.
3. select **"Save to PDF"**.
4. move or copy the PDF to your working directory.

### Step 2: Run the Script
run the script to process the PDF:

1. open a terminal or command prompt.
2. navigate to the folder containing the script.
3. execute the following command:  
   `python predict_mbti.py`

### Step 3: View the Results
the system will process the text and display detailed insights, including:

- **cleaned text preview**: a cleaned version of the extracted text.
- **MBTI prediction**: the most likely personality type.
- **confidence analysis**: confidence levels for each type.
- **psychometric insights**: detailed analysis of personality traits.
- **career suggestions**: industry-specific roles based on personality and traits.

## Example Output

```yaml
Cleaned Text: "results-driven professional with 10+ years in project management..."
Primary MBTI Prediction: INTJ
Supervisor Feedback: Most likely INTJ, 75% confident. Possible INTP, 25% confident.
Psychometric Insights:
  - Creativity: High
  - Leadership: Moderate
  - Risk Tolerance: Low
Career Suggestions:
  - Project Manager
  - Strategic Consultant
  - Business Analyst
