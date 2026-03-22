import streamlit as st
import re
import plotly.graph_objects as go

st.set_page_config(page_title="Misinformation Simulator", page_icon="🧠")

# -------- UI STYLE --------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

.title {
    font-size: 48px;
    text-align: center;
    font-weight: bold;
    color: white;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 30px;
}

textarea {
    border-radius: 10px !important;
    background-color: #0f172a !important;
    color: white !important;
    border: 1px solid #334155 !important;
}

div.stButton > button {
    background: linear-gradient(90deg, #6366f1, #06b6d4);
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
    font-weight: bold;
}

.metric-card {
    background: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.1);
}

</style>
""", unsafe_allow_html=True)

# -------- HEADER --------
st.markdown('<div class="title">🧠 Misinformation Simulator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Detect spam, clickbait & misleading patterns</div>', unsafe_allow_html=True)

text = st.text_area("Enter message / news / SMS")

# -------- HUGE KEYWORD SET --------
fake_weights = {

    # MONEY
    "earn money fast": 3, "make money fast": 3, "get rich quick": 3,
    "double your income": 3, "zero investment": 3,
    "guaranteed profit": 3, "instant profit": 3,

    # FREE / REWARD
    "free": 2, "win": 2, "winner": 2,
    "lottery": 3, "jackpot": 3,
    "claim now": 3, "limited offer": 3,
    "exclusive deal": 2.5,

    # URGENCY
    "act now": 3, "urgent": 2.5,
    "only today": 3, "before it's too late": 3,
    "last chance": 2.5,

    # CLICKBAIT
    "shocking": 2, "unbelievable": 2,
    "you won't believe": 2.5,
    "must watch": 2, "gone viral": 2,

    # CONSPIRACY
    "secret revealed": 2.5, "hidden truth": 2.5,
    "they don't want you to know": 3,
    "government is hiding": 3,

    # SPREAD
    "share this": 2.5, "forward this": 2.5,
    "send to everyone": 3,

    # CREDIBILITY
    "sources say": 1.5, "experts say": 1.5,
    "anonymous": 2, "rumor": 2.5,

    # HEALTH SCAM
    "miracle cure": 3, "no side effects": 3,
    "instant cure": 3, "100% cure": 3,

    # INTERNET SPAM
    "click here": 3, "visit now": 3,
    "buy now": 3, "order now": 3,

    # FEAR
    "warning": 2, "danger": 2,
    "alert": 2, "threat": 2,

    # UNREAL
    "alien": 3, "dragon": 3, "ghost": 3,

    # BANK / SMS SCAM
    "verify your account": 3,
    "update your details": 3,
    "account suspended": 3,
    "otp expired": 2.5,

    # DELIVERY SCAM
    "delivery failed": 3,
    "track your parcel": 2.5
}

real_keywords = [
    "official report", "government data",
    "confirmed", "according to",
    "study", "research", "analysis",
    "statistics", "investigation"
]

neutral_keywords = [
    "said", "recently", "news",
    "city", "visited", "reported",
    "event", "meeting"
]

# -------- FUNCTIONS --------
def fake_score_calc(text):
    score = 0
    reasons = []
    for k, w in fake_weights.items():
        if re.search(r'\b' + re.escape(k) + r'\b', text):
            score += w
            reasons.append(k)
    return score, reasons

def count_keywords(text, keywords):
    return sum(1 for k in keywords if k in text)

# -------- BUTTON --------
if st.button("Simulate & Analyze"):

    if not text.strip():
        st.warning("⚠️ Enter some text")
        st.stop()

    text_lower = text.lower()

    fake_score, reasons = fake_score_calc(text_lower)
    real_score = count_keywords(text_lower, real_keywords)
    neutral_score = count_keywords(text_lower, neutral_keywords)

    # EXTRA SIGNALS
    fake_score += text.count("!") * 0.5
    fake_score += sum(1 for w in text.split() if w.isupper()) * 0.5

    if "http" in text_lower or "www" in text_lower:
        fake_score += 2

    if len(text.split()) < 5:
        fake_score += 1

    # FIX ZERO ISSUE
    if fake_score == 0 and real_score == 0 and neutral_score == 0:
        neutral_score = 1

    # -------- RESULTS --------
    st.markdown("### 📊 Analysis Results")

    col1, col2, col3 = st.columns(3)

    col1.markdown(f'<div class="metric-card">Spam Score<br><b>{round(fake_score,2)}</b></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric-card">Info Score<br><b>{real_score}</b></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="metric-card">Neutral Score<br><b>{neutral_score}</b></div>', unsafe_allow_html=True)

    # DECISION
    if fake_score > 5:
        st.error("🚨 Likely Spam / Scam")
    elif real_score > 1 or neutral_score > 2:
        st.success("✅ Likely Normal Content")
    else:
        st.warning("⚖️ Mixed Signals")

    # REASONS
    if reasons:
        st.markdown("### 🔍 Detected Keywords")
        st.write(", ".join(reasons))

    # DONUT CHART
    fig = go.Figure(data=[go.Pie(
        labels=["Spam", "Info", "Neutral"],
        values=[fake_score, real_score, neutral_score],
        hole=0.5
    )])
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # BAR CHART
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=["Spam", "Info", "Neutral"],
        y=[fake_score, real_score, neutral_score]
    ))
    fig2.update_layout(template="plotly_dark", title="Score Comparison")
    st.plotly_chart(fig2, use_container_width=True)
