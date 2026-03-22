# 🧠 Misinformation Simulator

A Streamlit web application that analyzes text and simulates misinformation detection using a rule-based scoring system.

The app identifies patterns related to spam, scams, and misleading content, and shows results using simple visualizations.

---

## 🚀 Features

- Detects spam, scam, and clickbait patterns
- Uses weighted keywords for scoring
- Considers signals like punctuation, uppercase words, and links
- Displays results using charts (donut & bar)
- Simple and interactive UI

---

## ⚙️ How It Works

The app processes user input and checks for predefined keywords related to:

- Spam and scam indicators  
- Informational content  
- Neutral language  

Each keyword adds to a score based on its importance.

Additional signals like:
- Excessive `!`
- Fully capitalized words
- Presence of links
- Very short messages  

increase the spam score.

Based on the final scores, the app classifies the text as:
- Likely Spam / Scam  
- Likely Normal Content  
- Mixed Signals  

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- Plotly  
- Regex  

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
