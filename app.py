import streamlit as st
from graph import graph

st.set_page_config(
    page_title="AI Programming Quiz",
    page_icon="🧠",
    layout="wide"
)

# ================= CSS =================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

/* Main title */
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #38bdf8;
    margin-bottom: 20px;
}

/* Metric cards */
.metric-card {
    background: #0f172a;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid #38bdf8;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
    background: #38bdf8;
    color: white;
}

/* Radio group */
div[role="radiogroup"] {
    padding: 15px;
    border-radius: 12px;
    background: rgba(255,255,255,0.08);
}

/* Make all text white */
h1, h2, h3, h4, h5, h6,
p, span, div, label {
    color: white !important;
}

/* Question labels */
label[data-testid="stWidgetLabel"] p {
    color: #ffffff !important;
    font-size: 22px !important;
    font-weight: bold !important;
}

/* Radio options */
div[role="radiogroup"] label {
    color: #f8fafc !important;
    font-size: 18px !important;
    font-weight: 500 !important;
}

</style>
""", unsafe_allow_html=True)

# ================= Header =================
st.markdown(
    """
    <div class='main-title'>
        🧠 AI Programming Quiz Generator
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align:center;'>Generate AI-powered quizzes on any programming topic.</h4>",
    unsafe_allow_html=True
)

# ================= Session State =================
if "quiz" not in st.session_state:
    st.session_state.quiz = None

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# ================= Topic Input =================
topic = st.text_input(
    "Enter Topic",
    placeholder="Example: Array, Python, DBMS, OOPs, Recursion"
)

# ================= Generate Quiz =================
if st.button("🚀 Generate Quiz"):

    if not topic.strip():
        st.warning("Please enter a programming topic.")
        st.stop()

    with st.spinner("Generating Quiz..."):

        result = graph.invoke(
            {
                "topic": topic.strip()
            }
        )

        st.session_state.quiz = result["quiz"]
        st.session_state.submitted = False

# ================= Display Quiz =================
if st.session_state.quiz:

    st.subheader("📝 Quiz")

    for i, q in enumerate(st.session_state.quiz):

        st.markdown(
            f"""
            <div style="
                background:#1e293b;
                padding:15px;
                border-radius:12px;
                border:1px solid #38bdf8;
                margin-top:20px;
                margin-bottom:10px;
                color:white;
                font-size:22px;
                font-weight:bold;
            ">
                Q{i+1}. {q['question']}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.radio(
            "",
            q["options"],
            key=f"question_{i}",
            index=None,
            label_visibility="collapsed"
        )

    # ================= Submit =================
    if st.button("✅ Submit Quiz"):

        score = 0

        for i, q in enumerate(st.session_state.quiz):

            selected = st.session_state[f"question_{i}"]

            if selected == q["answer"]:
                score += 1

        percentage = round(
            (score / len(st.session_state.quiz)) * 100,
            2
        )

        correct = score
        wrong = len(st.session_state.quiz) - score

        if percentage >= 90:
            performance = "Excellent ⭐"

        elif percentage >= 70:
            performance = "Good 👍"

        elif percentage >= 50:
            performance = "Average 🙂"

        else:
            performance = "Needs Improvement 📚"

        # ================= Dashboard =================
        st.markdown("---")
        st.subheader("📊 Quiz Dashboard")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f"""
                <div class='metric-card'>
                    <h2>🎯 Score</h2>
                    <h1>{score}/{len(st.session_state.quiz)}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div class='metric-card'>
                    <h2>📈 Accuracy</h2>
                    <h1>{percentage}%</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.success(f"🏆 Performance: {performance}")
        st.info(f"📘 Topic: {topic}")

        st.write(f"✅ Correct Answers: {correct}")
        st.write(f"❌ Wrong Answers: {wrong}")

        # ================= Review =================
        st.markdown("---")
        st.subheader("📖 Answer Review")

        for i, q in enumerate(st.session_state.quiz):

            selected = st.session_state[f"question_{i}"]

            if selected == q["answer"]:
                st.success(f"Q{i+1}: Correct ✅")

            else:
                st.error(f"Q{i+1}: Wrong ❌")
                st.write(f"Your Answer: {selected}")
                st.write(f"Correct Answer: {q['answer']}")