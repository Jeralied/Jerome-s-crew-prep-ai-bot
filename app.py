import json
import random
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Crew Prep AI Bot",
    page_icon="✈️",
    layout="wide"
)


# =========================================================
# CUSTOM STYLING
# =========================================================

st.markdown("""
<style>

    .main {
        padding-top: 1rem;
    }

    .hero {
        padding: 2rem;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            #0b1f3a 0%,
            #123e63 100%
        );
        color: white;
        margin-bottom: 2rem;
    }

    .hero h1 {
        font-size: 42px;
        margin-bottom: 5px;
    }

    .hero p {
        font-size: 17px;
        opacity: 0.9;
    }

    .question-card {
        padding: 1.8rem;
        border-radius: 18px;
        border: 1px solid #dddddd;
        background: white;
        margin: 1rem 0;
    }

    .category {
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .tip-box {
        padding: 1rem;
        border-radius: 12px;
        background: #f4f7fb;
        border-left: 5px solid #123e63;
        margin-top: 1rem;
    }

    .stat-card {
        padding: 1rem;
        border-radius: 15px;
        border: 1px solid #dddddd;
        text-align: center;
        background: white;
    }

    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #777777;
        font-size: 14px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD QUESTIONS
# =========================================================

try:

    with open("questions.json", "r", encoding="utf-8") as file:
        questions = json.load(file)

except FileNotFoundError:

    st.error(
        "questions.json was not found. "
        "Make sure it is uploaded to the same GitHub repository as app.py."
    )

    st.stop()


# =========================================================
# SESSION STATE
# =========================================================

if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(questions)

if "questions_answered" not in st.session_state:
    st.session_state.questions_answered = 0

if "total_score" not in st.session_state:
    st.session_state.total_score = 0.0

if "last_score" not in st.session_state:
    st.session_state.last_score = None

if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = None

if "last_strengths" not in st.session_state:
    st.session_state.last_strengths = []

if "last_improvements" not in st.session_state:
    st.session_state.last_improvements = []


# =========================================================
# FUNCTIONS
# =========================================================

def get_new_question():

    current = st.session_state.current_question

    possible_questions = [
        question
        for question in questions
        if question["q"] != current["q"]
    ]

    if possible_questions:
        st.session_state.current_question = random.choice(
            possible_questions
        )
    else:
        st.session_state.current_question = random.choice(
            questions
        )

    st.session_state.last_score = None
    st.session_state.last_feedback = None
    st.session_state.last_strengths = []
    st.session_state.last_improvements = []


def evaluate_answer(answer):

    text = answer.lower()
    words = answer.split()

    score = 0
    strengths = []
    improvements = []

    # -----------------------------------------------------
    # ANSWER LENGTH
    # -----------------------------------------------------

    if len(words) >= 50:

        score += 1
        strengths.append(
            "Your answer contains good detail."
        )

    elif len(words) >= 30:

        score += 0.5

    else:

        improvements.append(
            "Add more detail to your answer."
        )


    # -----------------------------------------------------
    # KEYWORDS
    # -----------------------------------------------------

    keywords = {

        "safety":
            "You showed awareness of passenger safety.",

        "customer":
            "You demonstrated customer-service awareness.",

        "passenger":
            "You focused on the passenger experience.",

        "service":
            "You highlighted the importance of service.",

        "team":
            "You demonstrated teamwork awareness.",

        "communication":
            "You highlighted communication skills.",

        "calm":
            "You showed awareness of staying calm under pressure.",

        "professional":
            "You demonstrated professionalism.",

        "empathy":
            "You showed empathy toward customers or passengers.",

        "responsibility":
            "You demonstrated a sense of responsibility.",

        "adapt":
            "You showed adaptability."
    }


    for keyword, message in keywords.items():

        if keyword in text:

            score += 0.5
            strengths.append(message)


    # -----------------------------------------------------
    # STAR METHOD
    # -----------------------------------------------------

    star_words = [
        "situation",
        "task",
        "action",
        "result"
    ]

    star_count = sum(
        1 for word in star_words
        if word in text
    )

    if star_count >= 3:

        score += 1

        strengths.append(
            "Your answer shows elements of the STAR method."
        )

    else:

        improvements.append(
            "For experience questions, consider using the STAR method."
        )


    # -----------------------------------------------------
    # FINAL SCORE
    # -----------------------------------------------------

    score = min(
        5,
        round(score * 2) / 2
    )


    # -----------------------------------------------------
    # GENERAL FEEDBACK
    # -----------------------------------------------------

    if score >= 4:

        feedback = (
            "Excellent answer! You demonstrated several "
            "qualities that are important for cabin crew."
        )

    elif score >= 3:

        feedback = (
            "Good answer! You have a solid foundation, "
            "but you can make it stronger with a specific "
            "example and clearer structure."
        )

    elif score >= 2:

        feedback = (
            "Fair answer. You have some good points, "
            "but the interviewer would benefit from more "
            "detail and a stronger example."
        )

    else:

        feedback = (
            "Your answer needs improvement. Try to give "
            "a clearer, more detailed response and connect "
            "your answer to the cabin crew role."
        )


    # -----------------------------------------------------
    # DEFAULT IMPROVEMENTS
    # -----------------------------------------------------

    if not improvements:

        improvements.append(
            "Keep your answer natural and avoid sounding memorized."
        )

    improvements.append(
        "Speak clearly, maintain good eye contact, and show confidence."
    )


    return score, feedback, strengths, improvements


# =========================================================
# HERO SECTION
# =========================================================

st.markdown("""
<div class="hero">

    <h1>✈️ Crew Prep AI Bot</h1>

    <p>
        Practice cabin crew interviews, improve your answers,
        and build confidence before your big interview.
    </p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("🎯 Interview Practice")

    category_options = [
        "All Categories"
    ] + sorted(
        list(
            set(
                question["category"]
                for question in questions
            )
        )
    )

    selected_category = st.selectbox(
        "Choose a category",
        category_options
    )


    st.divider()


    st.subheader("📊 Your Progress")

    st.metric(
        "Questions Answered",
        st.session_state.questions_answered
    )

    st.metric(
        "Total Score",
        f"{st.session_state.total_score:.1f}"
    )


    if st.session_state.questions_answered > 0:

        average = (
            st.session_state.total_score
            / st.session_state.questions_answered
        )

        st.metric(
            "Average Score",
            f"{average:.1f}/5"
        )


    st.divider()


    st.subheader("💡 Interview Tip")

    st.write(
        "Don't memorize your answers word-for-word. "
        "Understand your examples and speak naturally."
    )


# =========================================================
# FILTER QUESTIONS
# =========================================================

if selected_category == "All Categories":

    available_questions = questions

else:

    available_questions = [
        question
        for question in questions
        if question["category"] == selected_category
    ]


# Make sure current question belongs to selected category

if (
    st.session_state.current_question
    not in available_questions
):

    st.session_state.current_question = random.choice(
        available_questions
    )


# =========================================================
# QUESTION SECTION
# =========================================================

question = st.session_state.current_question


st.subheader("🎤 Interview Question")


st.markdown(
    f"""
    <div class="question-card">

        <div class="category">
            {question["category"]}
        </div>

        <h2>
            {question["q"]}
        </h2>

        <div class="tip-box">
            <strong>💡 Interview Tip</strong><br><br>
            {question["tip"]}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# ANSWER AREA
# =========================================================

st.subheader("✍️ Your Answer")


answer = st.text_area(
    "Type your answer below:",
    height=220,
    placeholder=(
        "Imagine you are sitting in front of the interviewer. "
        "Write the answer you would actually give..."
    ),
    key="answer_box"
)


# =========================================================
# BUTTONS
# =========================================================

col1, col2, col3 = st.columns(3)


with col1:

    submit = st.button(
        "✅ Submit Answer",
        use_container_width=True
    )


with col2:

    next_question = st.button(
        "➡️ Next Question",
        use_container_width=True
    )


with col3:

    random_question = st.button(
        "🎲 Random Question",
        use_container_width=True
    )


# =========================================================
# SUBMIT ANSWER
# =========================================================

if submit:

    if len(answer.strip()) < 10:

        st.warning(
            "Your answer is too short. "
            "Try giving the interviewer more detail."
        )

    else:

        (
            score,
            feedback,
            strengths,
            improvements
        ) = evaluate_answer(answer)


        st.session_state.questions_answered += 1

        st.session_state.total_score += score

        st.session_state.last_score = score

        st.session_state.last_feedback = feedback

        st.session_state.last_strengths = strengths

        st.session_state.last_improvements = improvements


# =========================================================
# FEEDBACK SECTION
# =========================================================

if st.session_state.last_score is not None:

    st.divider()

    st.subheader("📋 Interview Feedback")


    score = st.session_state.last_score


    if score >= 4:

        st.success(
            f"⭐ Score: {score}/5 — Excellent!"
        )

    elif score >= 3:

        st.info(
            f"⭐ Score: {score}/5 — Good answer!"
        )

    else:

        st.warning(
            f"⭐ Score: {score}/5 — Keep improving!"
        )


    st.write(
        st.session_state.last_feedback
    )


    if st.session_state.last_strengths:

        st.markdown("### 💪 What You Did Well")

        for strength in st.session_state.last_strengths:

            st.write(
                f"✅ {strength}"
            )


    if st.session_state.last_improvements:

        st.markdown("### 🔧 How You Can Improve")

        for improvement in st.session_state.last_improvements:

            st.write(
                f"• {improvement}"
            )


# =========================================================
# STAR METHOD
# =========================================================

st.divider()

st.subheader("⭐ STAR Method")


st.write(
    "Use STAR when the interviewer asks you about "
    "a previous experience or difficult situation."
)


star_col1, star_col2, star_col3, star_col4 = st.columns(4)


with star_col1:

    st.markdown("### S")

    st.write("**Situation**")

    st.caption(
        "What was happening?"
    )


with star_col2:

    st.markdown("### T")

    st.write("**Task**")

    st.caption(
        "What were you responsible for?"
    )


with star_col3:

    st.markdown("### A")

    st.write("**Action**")

    st.caption(
        "What exactly did you do?"
    )


with star_col4:

    st.markdown("### R")

    st.write("**Result**")

    st.caption(
        "What happened because of your actions?"
    )


# =========================================================
# NEXT QUESTION LOGIC
# =========================================================

if next_question:

    get_new_question()

    st.rerun()


if random_question:

    if selected_category == "All Categories":

        st.session_state.current_question = random.choice(
            questions
        )

    else:

        st.session_state.current_question = random.choice(
            available_questions
        )

    st.session_state.last_score = None
    st.session_state.last_feedback = None
    st.session_state.last_strengths = []
    st.session_state.last_improvements = []

    st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        ✈️ Crew Prep AI Bot<br>

        Built to help aspiring cabin crew candidates
        practice with confidence.

    </div>
    """,
    unsafe_allow_html=True
)
