import html
import json
import random
import re
from pathlib import Path

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
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.25);
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

        .question-card,
        .result-card {
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
# LOAD AND VALIDATE QUESTIONS
# ============================================================

QUESTIONS_FILE = Path(__file__).resolve().parent / "questions.json"


@st.cache_data(show_spinner=False)
def load_questions():
    try:
        with QUESTIONS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

    except FileNotFoundError:
        return [], (
            "questions.json was not found. "
            "Make sure it is in the same folder as app.py."
        )

    except json.JSONDecodeError as error:
        return [], (
            "questions.json contains invalid JSON. "
            f"Check the formatting. Details: {error}"
        )

    if not isinstance(data, list):
        return [], (
            "questions.json must contain a list of question objects."
        )

    cleaned_questions = []

    for number, item in enumerate(data, start=1):

        if not isinstance(item, dict):
            continue

        category = str(item.get("category", "")).strip()
        question = str(item.get("q", "")).strip()
        tip = str(item.get("tip", "")).strip()

        if not category or not question:
            continue

        cleaned_questions.append(
            {
                "id": f"question-{number}",
                "category": category,
                "q": question,
                "tip": (
                    tip
                    or
                    "Answer naturally and support your response "
                    "with a relevant example when appropriate."
                ),
            }
        )

    if not cleaned_questions:
        return [], "No valid questions were found in questions.json."

    return cleaned_questions, None


questions, load_error = load_questions()

if load_error:
    st.error(f"❌ {load_error}")
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

if "asked_ids" not in st.session_state:
    st.session_state.asked_ids = []

if "session_history" not in st.session_state:
    st.session_state.session_history = []


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_categories():
    """Return all available question categories."""
    categories = sorted(
        {question["category"] for question in questions}
    )

    return ["All Categories"] + categories


def get_available_questions(category):
    """Return questions belonging to a selected category."""
    if category == "All Categories":
        return questions

    return [
        question
        for question in questions
        if question["category"] == category
    ]


def choose_question(category=None):
    """
    Choose a question while respecting the selected category
    and avoiding previously asked questions when possible.
    """

    if category is None:
        category = st.session_state.selected_category

    available = get_available_questions(category)

    if not available:
        available = questions

    current_id = st.session_state.current_question.get("id")

    # Prefer questions that have not appeared in this session.
    unseen_questions = [
        question
        for question in available
        if question["id"] not in st.session_state.asked_ids
        and question["id"] != current_id
    ]

    if unseen_questions:
        return random.choice(unseen_questions)

    # If all questions have been used, start another cycle.
    different_questions = [
        question
        for question in available
        if question["id"] != current_id
    ]

    if different_questions:
        return random.choice(different_questions)

    return random.choice(available)


def start_new_question():
    """Move to a new question and clear the previous feedback."""

    current_id = st.session_state.current_question.get("id")

    if current_id and current_id not in st.session_state.asked_ids:
        st.session_state.asked_ids.append(current_id)

    st.session_state.current_question = choose_question()

    st.session_state.answered = False
    st.session_state.last_score = None
    st.session_state.last_feedback = None


def reset_progress():
    """Reset the current practice session."""

    st.session_state.questions_answered = 0
    st.session_state.total_score = 0
    st.session_state.asked_ids = []
    st.session_state.session_history = []

    st.session_state.answered = False
    st.session_state.last_score = None
    st.session_state.last_feedback = None

    available = get_available_questions(
        st.session_state.selected_category
    )

    st.session_state.current_question = random.choice(
        available or questions
    )


def count_words(text):
    """Count words consistently throughout the application."""

    return len(
        re.findall(
            r"\b[\w'-]+\b",
            text,
        )
    )


def tokenize(text):
    """Return lowercase word tokens."""

    return set(
        re.findall(
            r"\b[a-zA-Z][a-zA-Z'-]*\b",
            text.lower(),
        )
    )


def contains_any(text, terms):
    """Check whether a complete word/phrase appears in text."""

    lower_text = text.lower()

    return any(
        re.search(
            rf"\b{re.escape(term)}\b",
            lower_text,
        )
        for term in terms
    )


# ============================================================
# ANSWER EVALUATION
# ============================================================

def evaluate_answer(answer, question):
    """
    Free, transparent, rule-based interview coaching.

    This is NOT an external AI model.
    It evaluates answer quality using:
    - detail
    - cabin-crew relevance
    - evidence/examples
    - structure
    - question category
    """

    answer = answer.strip()

    if not answer:
        return {
            "score": 0,
            "overall": "No answer was submitted.",
            "strengths": [],
            "improvements": [
                "Write a complete answer before submitting."
            ],
            "checks": [],
        }

    word_count = count_words(answer)
    lower_answer = answer.lower()
    tokens = tokenize(answer)

    category = question["category"].lower()

    # Categories where a real example/story is especially useful.
    behavioral_categories = {
        "teamwork",
        "situational",
        "experience",
        "customer service",
        "safety",
    }

    behavioral = category in behavioral_categories

    # --------------------------------------------------------
    # CATEGORY-SPECIFIC RELEVANCE
    # --------------------------------------------------------

    category_terms = {

        "general": {
            "professionalism",
            "communication",
            "passenger",
            "customer",
            "service",
            "safety",
            "teamwork",
            "career",
            "learn",
        },

        "customer service": {
            "customer",
            "passenger",
            "service",
            "listen",
            "empathy",
            "respect",
            "complaint",
            "solution",
            "assist",
            "calm",
        },

        "safety": {
            "safety",
            "procedure",
            "policy",
            "protocol",
            "crew",
            "passenger",
            "report",
            "emergency",
            "calm",
            "instruction",
        },

        "teamwork": {
            "team",
            "communication",
            "support",
            "collaborate",
            "respect",
            "listen",
            "help",
            "together",
            "colleague",
            "crew",
        },

        "situational": {
            "calm",
            "listen",
            "communicate",
            "professional",
            "safety",
            "assist",
            "inform",
            "supervisor",
            "solution",
            "respect",
        },

        "airline": {
            "airline",
            "passenger",
            "customer",
            "service",
            "safety",
            "brand",
            "culture",
            "crew",
            "learn",
            "professional",
        },

        "personal": {
            "strength",
            "improve",
            "learn",
            "experience",
            "goal",
            "professional",
            "communication",
            "teamwork",
            "service",
        },

        "experience": {
            "customer",
            "passenger",
            "team",
            "service",
            "handled",
            "solved",
            "learned",
            "result",
            "communication",
            "responsibility",
        },
    }

    default_terms = {
        "customer",
        "passenger",
        "service",
        "safety",
        "team",
        "communication",
        "professional",
    }

    relevance_terms = category_terms.get(
        category,
        default_terms,
    )

    matched_terms = [
        term
        for term in relevance_terms
        if term in tokens
    ]

    # --------------------------------------------------------
    # DETAIL
    # --------------------------------------------------------

    detail_ok = word_count >= 45
    detail_strong = word_count >= 80

    # --------------------------------------------------------
    # REAL EXAMPLE / EVIDENCE
    # --------------------------------------------------------

    evidence_patterns = [
        r"\bfor example\b",
        r"\bin my experience\b",
        r"\bwhen i\b",
        r"\bwhile i\b",
        r"\bduring\b",
        r"\bat work\b",
        r"\bin my role\b",
        r"\bi handled\b",
        r"\bi helped\b",
        r"\bi learned\b",
        r"\bi resolved\b",
        r"\bi worked\b",
        r"\bi dealt with\b",
        r"\bi assisted\b",
    ]

    evidence_ok = any(
        re.search(pattern, lower_answer)
        for pattern in evidence_patterns
    )

    # --------------------------------------------------------
    # STRUCTURE
    # --------------------------------------------------------

    structure_patterns = [
        r"\bfirst\b",
        r"\bthen\b",
        r"\bafter that\b",
        r"\bfinally\b",
        r"\bbecause\b",
        r"\bso that\b",
        r"\bas a result\b",
        r"\btherefore\b",
    ]

    structure_hits = sum(
        bool(re.search(pattern, lower_answer))
        for pattern in structure_patterns
    )

    structure_ok = structure_hits >= 1

    # --------------------------------------------------------
    # STAR SIGNALS
    # --------------------------------------------------------

    star_components = {
        "situation": bool(
            re.search(
                r"\b(when|during|while|situation)\b",
                lower_answer,
            )
        ),

        "task": bool(
            re.search(
                r"\b(task|responsible|responsibility|needed to)\b",
                lower_answer,
            )
        ),

        "action": bool(
            re.search(
                r"\b(i decided|i handled|i spoke|i helped|"
                r"i asked|i contacted|i explained|i assisted|"
                r"i resolved|i took)\b",
                lower_answer,
            )
        ),

        "result": bool(
            re.search(
                r"\b(result|outcome|resolved|improved|"
                r"learned|success|successfully)\b",
                lower_answer,
            )
        ),
    }

    star_hits = sum(star_components.values())

    # --------------------------------------------------------
    # SCORING
    # --------------------------------------------------------

    # Start at 1 and earn up to four additional points.
    score = 1

    strengths = []
    improvements = []

    # 1. Detail
    if detail_ok:

        score += 1

        if detail_strong:
            strengths.append(
                "You gave enough detail to develop your answer."
            )
        else:
            strengths.append(
                "Your answer has a reasonable amount of detail."
            )

    else:

        improvements.append(
            "Add more detail. For most questions, aim for roughly "
            "60–120 words."
        )

    # 2. Relevance
    if len(matched_terms) >= 2:

        score += 1

        if len(matched_terms) >= 4:
            strengths.append(
                "You connected your answer to several qualities "
                "relevant to cabin crew work."
            )
        else:
            strengths.append(
                "Your answer includes some relevant cabin-crew qualities."
            )

    else:

        improvements.append(
            "Connect your answer more clearly to qualities such as "
            "safety, service, communication, teamwork, empathy, "
            "and professionalism."
        )

    # 3. Evidence
    if evidence_ok:

        score += 1

        strengths.append(
            "You included language suggesting a real example or experience."
        )

    else:

        improvements.append(
            "Add a specific example from work, school, volunteering, "
            "or another real experience."
        )

    # 4. Structure
    if behavioral:

        if star_hits >= 2 or structure_ok:

            score += 1

            strengths.append(
                "Your answer has some structure, which helps an "
                "interviewer follow your story."
            )

        else:

            improvements.append(
                "For experience or situation questions, make the story "
                "clearer: Situation → Task → Action → Result."
            )

    else:

        if structure_ok:

            score += 1

            strengths.append(
                "Your answer has a clear logical flow."
            )

        else:

            improvements.append(
                "Use a simple structure: direct answer → "
                "reason/example → strong closing point."
            )

    score = min(5, max(1, score))

    # --------------------------------------------------------
    # OVERALL FEEDBACK
    # --------------------------------------------------------

    if score == 5:

        overall = (
            "Strong answer. It is detailed, relevant, and structured. "
            "Keep it natural rather than memorizing it word-for-word."
        )

    elif score == 4:

        overall = (
            "Very good answer. You have a solid foundation; "
            "strengthen the one or two areas shown below."
        )

    elif score == 3:

        overall = (
            "Good starting point. Add stronger evidence, relevance, "
            "or structure to make the answer more convincing."
        )

    elif score == 2:

        overall = (
            "Your answer needs more development. Add a specific "
            "example and show how your actions helped the customer, "
            "team, or situation."
        )

    else:

        overall = (
            "Your answer needs significant development. "
            "Give a complete response and connect it directly "
            "to the question."
        )

    checks = [
        f"Length: {word_count} words",
        f"Relevant terms detected: {len(matched_terms)}",
        (
            "Real-example signal: Yes"
            if evidence_ok
            else "Real-example signal: Not detected"
        ),
        (
            "Structure signal: Yes"
            if structure_ok
            else "Structure signal: Not detected"
        ),
    ]

    return {
        "score": score,
        "overall": overall,
        "strengths": strengths,
        "improvements": improvements,
        "checks": checks,
    }


# ============================================================
# DISPLAY FEEDBACK
# ============================================================

def display_feedback(feedback):

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
                    {html.escape(feedback["overall"])}
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
                    ✓ {html.escape(strength)}
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
                    → {html.escape(improvement)}
                </div>
                """,
                unsafe_allow_html=True,
            )

    # --------------------------------------------------------
    # TECHNICAL EVALUATION DETAILS
    # --------------------------------------------------------

    if feedback.get("checks"):

        with st.expander("🔍 Evaluation details"):

            for check in feedback["checks"]:
                st.write(f"• {check}")

    # --------------------------------------------------------
    # STAR METHOD
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="star-box">

            <div class="star-title">
                ⭐ STAR Method
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
                Explain the outcome or what you learned.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-badge">
            ✈️ CABIN CREW INTERVIEW TRAINING
        </div>

        <h1>
            Crew Prep AI
        </h1>

        <p>
            Practice realistic cabin crew interview questions,
            improve your answers, and build confidence before
            your airline interview.
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

    st.caption(
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

    # Change category
    if selected_category != st.session_state.selected_category:

        st.session_state.selected_category = selected_category

        available = get_available_questions(
            selected_category
        )

        if available:
            st.session_state.current_question = random.choice(
                available
            )

        st.session_state.answered = False
        st.session_state.last_score = None
        st.session_state.last_feedback = None

        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

    st.markdown("### 📊 Your Progress")

    questions_answered = (
        st.session_state.questions_answered
    )

    average_score = (
        st.session_state.total_score
        / questions_answered
        if questions_answered
        else 0
    )

    st.metric(
        "Questions answered",
        questions_answered,
    )

    st.metric(
        "Average score",
        f"{average_score:.1f} / 5",
    )

    st.divider()

    # --------------------------------------------------------
    # RESET
    # --------------------------------------------------------

    if st.button(
        "🔄 Reset Progress",
        use_container_width=True,
    ):

        reset_progress()
        st.rerun()

    st.divider()

    st.markdown(
        """
        <div style="font-size:13px; opacity:0.75;">

            <b>Interview Tip:</b><br>

            Speak naturally. Don't memorize answers
            word-for-word.

            <br><br>

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

    average_score = (
        st.session_state.total_score
        / st.session_state.questions_answered
        if st.session_state.questions_answered
        else 0
    )

    st.metric(
        "🎯 Your Average",
        (
            f"{average_score:.1f}/5"
            if st.session_state.questions_answered
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

    question_position = next(
        index + 1
        for index, item in enumerate(
            available_questions
        )
        if item["id"] == question["id"]
    )

except StopIteration:

    question_position = 1


st.markdown(
    f"""
    <div class="question-card">

        <div class="category-label">
            {html.escape(question["category"])}
        </div>

        <div class="question-number">
            Question {question_position}
            of {len(available_questions)}
        </div>

        <div class="question-text">
            {html.escape(question["q"])}
        </div>

        <div class="tip-box">

            <span class="tip-title">
                💡 Interview Tip
            </span>

            <br>

            {html.escape(question["tip"])}

        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# ANSWER AREA
# ============================================================

st.markdown("### 📝 Your Answer")

# IMPORTANT:
# Each question gets its own widget key.
# This prevents an old answer from appearing
# when the user moves to a new question.

answer_key = (
    f"answer_{question['id']}"
)

answer = st.text_area(
    "Type your interview answer below:",
    height=210,
    key=answer_key,
    placeholder=(
        "Imagine you are sitting in front of "
        "the recruiter. Answer naturally and "
        "professionally..."
    ),
    disabled=st.session_state.answered,
)

word_count = count_words(answer)

st.caption(
    f"{word_count} words"
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

        st.session_state.last_score = (
            feedback["score"]
        )

        st.session_state.last_feedback = feedback

        st.session_state.answered = True

        st.session_state.questions_answered += 1

        st.session_state.total_score += (
            feedback["score"]
        )

        # Save session history.
        st.session_state.session_history.append(
            {
                "question_id": question["id"],
                "question": question["q"],
                "category": question["category"],
                "score": feedback["score"],
            }
        )

        st.rerun()


# ============================================================
# NEXT QUESTION / RANDOM QUESTION
# ============================================================

if next_question or random_question:

    start_new_question()

    st.rerun()


# ============================================================
# FEEDBACK
# ============================================================

if st.session_state.last_feedback:

    display_feedback(
        st.session_state.last_feedback
    )

    if st.button(
        "🚀 Practice Another Question",
        type="primary",
        use_container_width=True,
    ):

        start_new_question()

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
