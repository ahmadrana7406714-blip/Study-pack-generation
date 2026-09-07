import os
import streamlit as st

from workflow import generate_study_pack

st.set_page_config(
    page_title="AI Study Pack Generator",
    page_icon="📚",
    layout="wide",
)

st.title("📚 AI Study Pack Generator")
st.caption("Multi-stage AI workflow: Planning → Content → Assessment → Review → Refinement")

# ---------------------------
# API configuration
# ---------------------------
# For Streamlit Cloud, add these in:
# App → Settings → Secrets
#
# GROQ_API_KEY = "your_key"
# GROQ_BASE_URL = "https://api.groq.com/openai/v1"
#
# Or use:
# OPENAI_API_KEY = "your_key"
# OPENAI_BASE_URL = "https://api.openai.com/v1"

if hasattr(st, "secrets"):
    for key in ["GROQ_API_KEY", "GROQ_BASE_URL", "OPENAI_API_KEY", "OPENAI_BASE_URL"]:
        if key in st.secrets and key not in os.environ:
            os.environ[key] = str(st.secrets[key])

with st.sidebar:
    st.header("⚙️ AI Settings")

    model = st.text_input(
        "Model",
        value="llama-3.3-70b-versatile",
        help="Use a model supported by your selected OpenAI-compatible provider.",
    )

    st.markdown("---")
    st.subheader("Workflow")
    st.write("1. 🗺️ Planning")
    st.write("2. 📝 Content Generation")
    st.write("3. ❓ Assessment")
    st.write("4. 🔍 Review")
    st.write("5. ✨ Refinement")

st.subheader("Tell us what you want to learn")

col1, col2 = st.columns(2)

with col1:
    topic = st.text_input(
        "Topic / Subject",
        placeholder="e.g. Python Programming",
    )

    level = st.selectbox(
        "Skill Level",
        ["Beginner", "Intermediate", "Advanced"],
    )

with col2:
    duration = st.text_input(
        "Study Duration",
        placeholder="e.g. 4 weeks",
    )

    goal = st.text_area(
        "Learning Goal",
        placeholder="e.g. I want to learn Python for data science.",
        height=100,
    )

generate = st.button(
    "🚀 Generate Personalized Study Pack",
    type="primary",
    use_container_width=True,
)

if generate:
    if not topic.strip():
        st.error("Please enter a topic or subject.")
        st.stop()

    if not duration.strip():
        st.error("Please enter a study duration.")
        st.stop()

    if not goal.strip():
        st.error("Please enter your learning goal.")
        st.stop()

    progress = st.progress(0)
    status = st.empty()

    try:
        status.info("🗺️ Stage 1/5 — Creating personalized study plan...")
        progress.progress(10)

        # The workflow itself executes all stages.
        result = generate_study_pack(
            topic=topic,
            level=level,
            duration=duration,
            goal=goal,
            model=model,
        )

        status.info("📝 Stage 2/5 — Content generated.")
        progress.progress(35)

        status.info("❓ Stage 3/5 — Assessment generated.")
        progress.progress(55)

        status.info("🔍 Stage 4/5 — Quality review completed.")
        progress.progress(75)

        status.info("✨ Stage 5/5 — Final refinement completed.")
        progress.progress(100)

        status.success("Study pack generated successfully!")

        st.markdown("---")
        st.header("📦 Final Personalized Study Pack")
        st.markdown(result["final_pack"])

        # Optional workflow trace for demonstration/project presentation.
        st.markdown("---")
        st.subheader("🔄 AI Workflow Trace")

        with st.expander("🗺️ 1. Planning Output"):
            st.markdown(result["plan"])

        with st.expander("📝 2. Content Generation Output"):
            st.markdown(result["content"])

        with st.expander("❓ 3. Assessment Output"):
            st.markdown(result["assessment"])

        with st.expander("🔍 4. Review Output"):
            st.markdown(result["review"])

    except Exception as e:
        progress.empty()
        status.empty()

        st.error("The workflow could not be completed.")
        st.warning(
            "Check your API key, base URL, model name, internet connection, "
            "and provider limits."
        )

        # Show a concise error for debugging without crashing the app.
        with st.expander("Technical error"):
            st.code(str(e))

st.markdown("---")
st.caption("AI Study Pack Generator • Multi-stage AI Workflow")
