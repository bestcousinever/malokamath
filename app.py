import random
import streamlit as st

st.set_page_config(page_title="mochaiato 💙", page_icon="💙", layout="centered")

st.markdown("""
<style>
.stApp, [data-testid="stAppViewContainer"] {background: #EAF0F9;}
[data-testid="stHeader"] {background: #EAF0F9;}
h1, h2, h3 {color: #102A56 !important;}
.stApp p, .stApp label {color: #18365D;}
.stButton > button, div[data-testid="stFormSubmitButton"] button {
    background: #173B78 !important; color: white !important;
    border: 0 !important; border-radius: 12px !important;
    font-weight: 700 !important;
}
.stButton > button:hover, div[data-testid="stFormSubmitButton"] button:hover {
    background: #2858A0 !important; color: white !important;
}
[data-testid="stForm"] {background: #F8FAFF; border: 1px solid #B8CBE7; border-radius: 16px;}
</style>
""", unsafe_allow_html=True)

WIN_SCORE = 50

DEFAULTS = {
    "started": False,
    "operation": "multiplication",
    "multiplication_level": 2,
    "division_level": 2,
    "multiplication_correct": 0,
    "multiplication_wrong": 0,
    "division_correct": 0,
    "division_wrong": 0,
    "number1": None,
    "number2": None,
    "answered": False,
    "feedback": "",
    "was_correct": False,
    "score": 0,
    "questions": 0,
    "question_id": 0,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


def new_question():
    s = st.session_state
    level = s[f"{s.operation}_level"]
    if level == 1:
        low, high = 1, 10
    elif level == 2:
        low, high = 10, 50
    else:
        low, high = 50, 100
    s.number1 = random.randint(low, high)
    s.number2 = random.randint(low, high)  # Never zero, so division is safe
    s.answered = False
    s.feedback = ""
    s.question_id += 1


def check_answer(answer):
    s = st.session_state
    op = s.operation
    actual = s.number1 * s.number2 if op == "multiplication" else s.number1 / s.number2
    expected = actual if op == "multiplication" else round(actual, 1)
    correct = (answer == expected)
    s.questions += 1
    s.was_correct = correct

    if correct:
        s.score += 1
        s[f"{op}_correct"] += 1
        s[f"{op}_wrong"] = 0
        s.feedback = "🌟 Correct! You're crushing it!"
        if s[f"{op}_correct"] >= 3:
            if s[f"{op}_level"] < 3:
                s[f"{op}_level"] += 1
                s.feedback += " 🎉 Level up!"
            s[f"{op}_correct"] = 0
    else:
        symbol = "×" if op == "multiplication" else "÷"
        s.feedback = f"Not quite! {s.number1} {symbol} {s.number2} = {expected:g}. 💙"
        s[f"{op}_wrong"] += 1
        s[f"{op}_correct"] = 0
        if s[f"{op}_wrong"] >= 3:
            if s[f"{op}_level"] > 1:
                s[f"{op}_level"] -= 1
                s.feedback += " We'll practice an easier level next time."
            s[f"{op}_wrong"] = 0
    s.answered = True


st.title("i love tala")
st.write("Multiplication, division, and a little friendly competition. ✨")
s = st.session_state

if not s.started:
    st.subheader("Ready to show off your math skills?")
    st.write("Three correct answers in a row levels you up. Three wrong answers in a row lowers the difficulty. Each operation has its own level!")
    if st.button("🚀 Let's go!", use_container_width=True):
        s.started = True
        new_question()
        st.rerun()
else:
    if s.number1 is None:
        new_question()

    op = s.operation
    level = s[f"{op}_level"]
    symbol = "×" if op == "multiplication" else "÷"
    st.write(f"⭐ **Correct answers:** {s.score} / {WIN_SCORE}  ·  **Questions played:** {s.questions}")
    st.progress(min(s.score / WIN_SCORE, 1.0), text=f"🏆 {min(s.score, WIN_SCORE)} of {WIN_SCORE} correct answers")
    st.write(f"✖️ **Multiplication:** Level {s.multiplication_level}　|　➗ **Division:** Level {s.division_level}")
    if s.score >= WIN_SCORE:
        st.balloons()
        st.success("🏆 YOU WIN, i am the best friend ever 💙 50 correct answers! You are a math legend! 🎉")
        st.write(f"You answered **{s.score}** questions correctly out of **{s.questions}** total questions. Amazing work!")
        if st.button("💙 Play again", use_container_width=True):
            for key, value in DEFAULTS.items():
                s[key] = value
            st.rerun()
        st.stop()

    st.subheader(f"{'✖️ Multiplication' if op == 'multiplication' else '➗ Division'} — Level {level}")
    st.markdown(f"## {s.number1} {symbol} {s.number2} = ?")

    if not s.answered:
        if op == "division":
            st.caption("Round your answer to 1 decimal place (e.g. 0.3).")
        with st.form(key=f"question_{s.question_id}"):
            answer = st.number_input(
                "Your answer",
                value=0.0 if op == "division" else 0,
                step=0.1 if op == "division" else 1,
                format="%.1f" if op == "division" else "%d",
            )
            submitted = st.form_submit_button("💙 Check answer", use_container_width=True)
        if submitted:
            check_answer(answer)
            st.rerun()
    else:
        if s.was_correct:
            st.success(s.feedback)
        else:
            st.info(s.feedback)
        if st.button("➡️ Next question", use_container_width=True):
            s.operation = "division" if op == "multiplication" else "multiplication"
            new_question()
            st.rerun()

    st.divider()
    if st.button("🔄 Restart game"):
        for key, value in DEFAULTS.items():
            s[key] = value
        st.rerun()
