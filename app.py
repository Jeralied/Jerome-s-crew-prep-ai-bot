```python
import json
import random
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Crew Prep AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GENERAL ---------- */

    .stApp {
        background: #f5f7fa;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ---------- HERO ---------- */

    .hero {
        background: linear-gradient(135deg, #102a43, #1f4e79);
        padding: 42px 38px;
        border-radius: 22px;
        margin-bottom: 25px;
        color: white;
        box-shadow: 0 10px 30px rgba(16, 42, 67, 0.18);
    }

    .hero h1 {
        font-size: 42px;
        margin: 0 0 8px 0;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .hero p {
        font-size: 18px;
        margin: 0;
        opacity: 0.92;
        line-height: 1.6;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.25);
        padding: 7px 13px;
        border-radius: 999px;
        font-size: 13px;
        margin-bottom: 14px;
    }

    /* ---------- QUESTION CARD ---------- */

    .question-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 30px;
        margin-top: 10px;
        margin-bottom: 20px;
        box-shadow: 0 7px 25px rgba(15, 23, 42, 0.07);
    }

    .category-label {
        display: inline-block;
        background: #e8f1fb;
        color: #1f4e79;
        font-weight: 700;
        font-size: 13px;
        padding: 6px 12px;
        border-radius: 999px;
        margin-bottom: 15px;
    }

    .question-number {
        color: #64748b;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .question-text {
        color: #102a43;
        font-size: 28px;
        line-height: 1.35;
        font-weight: 750;
        margin-bottom: 18px;
    }

    /* ---------- TIP ---------- */

    .tip-box {
        background: #f8fafc;
        border-left: 4px solid #2f8f7e;
        border-radius: 10px;
        padding: 15px 17px;
        color: #475569;
        font-size: 14px;
        line-height: 1.6;
        margin-top: 12px;
    }

    .tip-title {
        font-weight: 800;
        color: #1e293b;
    }

    /* ---------- RESULT CARDS ---------- */

    .result-card {
        background: white;
        border-radius: 16px;
        padding: 22px;
        border: 1px solid #e2e8f0;
        margin-top: 15px;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.06);
    }

    .score-number {
        font-size: 48px;
        font-weight: 800;
        color: #1f4e79;
        line-height: 1;
    }

    .score-label {
        color: #64748b;
        font-size: 14px;
        margin-top: 5px;
    }

    .strength {
        background: #ecfdf5;
        border-left: 4px solid #2f8f7e;
        padding: 12px 15px;
        border-radius: 8px;
        margin: 7px 0;
        color: #166534;
    }

    .weakness {
        background: #fff7ed;
        border-left: 4px solid #f59e0b;
        padding: 12px 15px;
        border-radius: 8px;
        margin: 7px 0;
        color: #9a3412;
    }

    /* ---------- STAR BOX ---------- */

    .star-box {
        background: #eef4fb;
        border: 1px solid #d7e4f2;
        border-radius: 14px;
        padding: 20px;
        margin-top: 18px;
    }

    .star-title {
        color: #102a43;
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .star-item {
        margin: 7px 0;
        color: #334155;
        line-height: 1.5;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #102a43;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        border-radius: 10px;
        font-weight: 700;
        min-height: 44px;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 13px;
        padding-top: 35px;
        padding-bottom: 10px;
    }

    /* ---------- MOBILE ---------- */

    @media (max-width: 700px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero {
            padding: 28px 22px;
            border-radius: 17px;
        }

        .hero h1 {
            font-size: 31px;
        }

        .hero p {
            font-size: 15px;
        }

        .question-card {
            padding: 22px;
        }

        .question-text {
            font-size: 22px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOAD QUESTIONS
# ============================================================

@st.cache_data
def load_questions():
    try:
        with open("questions.json", "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        st.error(
            "❌ questions.json was not found. "
            "Make sure questions.json is in the same folder as app.py."
        )
        return []

    except json.JSONDecodeError:
        st.error(
            "❌ questions.json contains invalid JSON. "
            "Please check the file formatting."
        )
        return []


questions = load_questions()


# Stop the app if questions cannot be loaded.
if not questions:
    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(questions)

if "answered" not in st.session_state:
    st.session_state.answered = False

if "last_score" not in st.session_state:
    st.session_state.last_score = None

if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = None

if "questions_answered" not in st.session_state:
    st.session_state.questions_answered = 0

if "total_score" not in st.session_state:
    st.session_state.total_score = 0

if "selected_category" not in st.session_state:
    st.session_state.selected_category = "All Categories"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_categories():
    categories = sorted(
        list(set(question["category"] for question in questions))
    )
    return ["All Categories"] + categories


def get_available_questions(category):
    if category == "All Categories":
        return questions

    return [
        question
        for question in questions
        if question["category"] == category
    ]


def choose_question(category=None):
    """
    Choose a random question while respecting the selected category.
    """

    if category is None:
        category = st.session_state.selected_category

    available = get_available_questions(category)

    if not available:
        available = questions

    # Try not to show exactly the same question twice in a row.
    if len(available) > 1:
        possible_questions = [
            q
            for q in available
            if q != st.session_state.current_question
        ]

        if possible_questions:
            return random.choice(possible_questions)

    return random.choice(available)


def reset_question():
    st.session_state.current_question = choose_question()
    st.session_state.answered = False
    st.session_state.last_score = None
    st.session_state.last_feedback = None


def evaluate_answer(answer, question):
    """
    Simple interview-answer evaluation.

    This version does not require an external AI API.
    It evaluates the answer using useful interview indicators.
    """

    answer = answer.strip()

    if not answer:
        return {
            "score": 0,
            "strengths": ["You did not provide an answer yet."],
            "improvements": [
                "Write a complete answer before submitting."
            ],
        }

    words = answer.split()
    word_count = len(words)

    score = 1
    strengths = []
    improvements = []

    # --------------------------------------------------------
    # LENGTH
    # --------------------------------------------------------

    if word_count >= 80:
        score += 1
        strengths.append(
            "Your answer has enough detail to develop your point."
        )

    elif word_count >= 45:
        score += 1
        strengths.append(
            "Your answer provides a reasonable amount of detail."
        )

    else:
        improvements.append(
            "Try to give more detail. Aim for roughly 60–120 words "
            "for most interview answers."
        )

    # --------------------------------------------------------
    # CUSTOMER SERVICE / PROFESSIONAL LANGUAGE
    # --------------------------------------------------------

    positive_terms = [
        "customer",
        "passenger",
        "service",
        "safety",
        "team",
        "teamwork",
        "communication",
        "professional",
        "calm",
        "respect",
        "help",
        "assist",
        "experience",
        "solution",
        "listen",
        "empathy",
        "responsibility",
        "adapt",
        "learn",
    ]

    lower_answer = answer.lower()

    matched_terms = [
        term for term in positive_terms
        if term in lower_answer
    ]

    if len(matched_terms) >= 4:
        score += 1
        strengths.append(
            "You used language that is relevant to cabin crew and "
            "customer-facing work."
        )

    else:
        improvements.append(
            "Connect your answer more clearly to cabin crew qualities "
            "such as safety, service, teamwork, communication, empathy, "
            "and professionalism."
        )

    # --------------------------------------------------------
    # EXAMPLE / EVIDENCE
    # --------------------------------------------------------

    evidence_terms = [
        "when",
        "while",
        "because",
        "for example",
        "experience",
        "worked",
        "handled",
        "helped",
        "during",
        "situation",
    ]

    evidence_count = sum(
        1 for term in evidence_terms
        if term in lower_answer
    )

    if evidence_count >= 2:
        score += 1
        strengths.append(
            "You included evidence or an example rather than relying "
            "only on general statements."
        )

    else:
        improvements.append(
            "Where possible, include a real example from your work, "
            "school, volunteering, or other experience."
        )

    # --------------------------------------------------------
    # STAR / STRUCTURE
    # --------------------------------------------------------

    star_terms = [
        "situation",
        "task",
        "action",
        "result",
    ]

    star_matches = sum(
        1 for term in star_terms
        if term in lower_answer
    )

    if star_matches >= 2:
        score += 1
        strengths.append(
            "Your answer shows signs of a structured STAR-style response."
        )

    else:
        improvements.append(
            "For experience-based questions, structure your answer "
            "using Situation, Task, Action, and Result."
        )

    # Keep score between 1 and 5.
    score = max(1, min(score, 5))

    # --------------------------------------------------------
    # SCORE-BASED FEEDBACK
    # --------------------------------------------------------

    if score == 5:
        overall = (
            "Excellent answer. It is detailed, relevant, and shows "
            "strong interview awareness."
        )

    elif score == 4:
        overall = (
            "Very good answer. With a little more structure or detail, "
            "it could become excellent."
        )

    elif score == 3:
        overall = (
            "Good starting point. Your answer has useful content, "
            "but it needs stronger evidence or structure."
        )

    elif score == 2:
        overall = (
            "Your answer needs more development. Try adding a specific "
            "example and connecting it to cabin crew responsibilities."
        )

    else:
        overall = (
            "Your answer needs significant improvement. Give a complete "
            "professional response and support your points with examples."
        )

    return {
        "score": score,
        "overall": overall,
        "strengths": strengths,
        "improvements": improvements,
    }


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">✈️ CABIN CREW INTERVIEW TRAINING</div>
        <h1>Crew Prep AI</h1>
        <p>
            Practice realistic cabin crew interview questions,
            improve your answers, and build confidence before your
            airline interview.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ✈️ Crew Prep")

    st.markdown(
        "Prepare for your next cabin crew interview."
    )

    st.divider()

    st.markdown("### Practice Settings")

    categories = get_categories()

    selected_category = st.selectbox(
        "Question category",
        categories,
        index=categories.index(
            st.session_state.selected_category
        ),
    )

    # If category changes, immediately select a question
    # from the new category.
    if selected_category != st.session_state.selected_category:

        st.session_state.selected_category = selected_category

        available = get_available_questions(selected_category)

        if available:
            st.session_state.current_question = random.choice(
                available
            )

        st.session_state.answered = False
        st.session_state.last_score = None
        st.session_state.last_feedback = None

        st.rerun()

    st.divider()

    st.markdown("### 📊 Your Progress")

    questions_answered = st.session_state.questions_answered

    if questions_answered > 0:
        average_score = (
            st.session_state.total_score
            / questions_answered
        )
    else:
        average_score = 0

    st.metric(
        "Questions answered",
        questions_answered,
    )

    st.metric(
        "Average score",
        f"{average_score:.1f} / 5",
    )

    st.divider()

    if st.button(
        "🔄 Reset Progress",
        use_container_width=True,
    ):
        st.session_state.questions_answered = 0
        st.session_state.total_score = 0
        st.session_state.last_score = None
        st.session_state.last_feedback = None
        st.session_state.answered = False
        st.session_state.current_question = choose_question()

        st.rerun()

    st.markdown(
        """
        <div style="margin-top:25px; font-size:13px; opacity:0.75;">
            <b>Tip:</b><br>
            Speak naturally. Don't memorize answers word-for-word.
            Use real experiences whenever possible.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# TOP STATISTICS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "✈️ Interview Questions",
        len(questions),
    )

with col2:
    st.metric(
        "📚 Categories",
        len(get_categories()) - 1,
    )

with col3:
    st.metric(
        "🎯 Your Average",
        (
            f"{st.session_state.total_score / st.session_state.questions_answered:.1f}/5"
            if st.session_state.questions_answered > 0
            else "—"
        ),
    )


# ============================================================
# CURRENT QUESTION
# ============================================================

question = st.session_state.current_question

available_questions = get_available_questions(
    st.session_state.selected_category
)

try:
    question_position = (
        available_questions.index(question) + 1
    )
except ValueError:
    question_position = 1


st.markdown(
    f"""
    <div class="question-card">

        <div class="category-label">
            {question["category"]}
        </div>

        <div class="question-number">
            Interview Question
        </div>

        <div class="question-text">
            {question["q"]}
        </div>

        <div class="tip-box">
            <span class="tip-title">💡 Interview Tip</span><br>
            {question["tip"]}
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# ANSWER AREA
# ============================================================

st.markdown("### 📝 Your Answer")

answer = st.text_area(
    "Type your interview answer below:",
    height=210,
    placeholder=(
        "Imagine you are sitting in front of the recruiter. "
        "Answer naturally and professionally..."
    ),
    disabled=st.session_state.answered,
)


# ============================================================
# ACTION BUTTONS
# ============================================================

button_col1, button_col2, button_col3 = st.columns(
    [1.5, 1.2, 1.2]
)

with button_col1:

    submit = st.button(
        "🎯 Submit Answer",
        type="primary",
        use_container_width=True,
        disabled=st.session_state.answered,
    )

with button_col2:

    next_question = st.button(
        "➡️ Next Question",
        use_container_width=True,
    )

with button_col3:

    random_question = st.button(
        "🎲 Random",
        use_container_width=True,
    )


# ============================================================
# SUBMIT ANSWER
# ============================================================

if submit:

    if not answer.strip():

        st.warning(
            "Please type an answer before submitting."
        )

    else:

        feedback = evaluate_answer(
            answer,
            question,
        )

        st.session_state.last_score = feedback["score"]
        st.session_state.last_feedback = feedback
        st.session_state.answered = True

        st.session_state.questions_answered += 1
        st.session_state.total_score += feedback["score"]

        st.rerun()


# ============================================================
# NEXT QUESTION
# ============================================================

if next_question:

    reset_question()
    st.rerun()


# ============================================================
# RANDOM QUESTION
# ============================================================

if random_question:

    reset_question()
    st.rerun()


# ============================================================
# FEEDBACK
# ============================================================

if st.session_state.last_feedback:

    feedback = st.session_state.last_feedback
    score = feedback["score"]

    st.divider()

    st.markdown("## 🎯 Interview Feedback")

    result_col1, result_col2 = st.columns(
        [1, 2.5]
    )

    with result_col1:

        st.markdown(
            f"""
            <div class="result-card">
                <div class="score-number">
                    {score}/5
                </div>
                <div class="score-label">
                    Interview Score
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with result_col2:

        st.markdown(
            f"""
            <div class="result-card">
                <strong>Overall Feedback</strong>
                <p style="color:#475569; line-height:1.6;">
                    {feedback["overall"]}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # STRENGTHS
    # --------------------------------------------------------

    st.markdown("### 💪 Strengths")

    if feedback["strengths"]:

        for strength in feedback["strengths"]:

            st.markdown(
                f"""
                <div class="strength">
                    ✓ {strength}
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:

        st.info(
            "Keep practicing and look for ways to make your "
            "answers more specific."
        )

    # --------------------------------------------------------
    # IMPROVEMENTS
    # --------------------------------------------------------

    st.markdown("### 🔧 Areas to Improve")

    if feedback["improvements"]:

        for improvement in feedback["improvements"]:

            st.markdown(
                f"""
                <div class="weakness">
                    → {improvement}
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:

        st.success(
            "No major improvement areas were detected."
        )

    # --------------------------------------------------------
    # STAR METHOD
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="star-box">

            <div class="star-title">
                ⭐ Use the STAR Method
            </div>

            <div class="star-item">
                <b>S — Situation:</b>
                Briefly explain what was happening.
            </div>

            <div class="star-item">
                <b>T — Task:</b>
                Explain what you were responsible for.
            </div>

            <div class="star-item">
                <b>A — Action:</b>
                Explain exactly what you did.
            </div>

            <div class="star-item">
                <b>R — Result:</b>
                Explain the positive outcome or what you learned.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")

    if st.button(
        "🚀 Practice Another Question",
        type="primary",
        use_container_width=True,
    ):

        reset_question()
        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        ✈️ Crew Prep AI · Cabin Crew Interview Practice
        <br>
        Practice • Improve • Prepare • Fly
    </div>
    """,
    unsafe_allow_html=True,
)
```
