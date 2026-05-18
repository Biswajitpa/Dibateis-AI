import streamlit as st
from google import genai

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Diabetes Medical Chatbot",
    page_icon="🩺",
    layout="centered"
)

# =========================
# LOAD API KEY
# =========================
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ GEMINI_API_KEY not found in secrets.toml")
    st.stop()

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# =========================
# GEMINI CLIENT
# =========================
try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    st.error(f"Error creating Gemini client: {e}")
    st.stop()

# =========================
# ASK GEMINI FUNCTION
# =========================
def ask_gemini(query):

    prompt = f"""
You are a diabetes medical assistant chatbot.

Rules:
- Answer ONLY diabetes-related questions
- Give short, simple, safe medical information
- If question is unrelated, politely refuse

User Question:
{query}
"""

    try:
        # ✅ WORKING MODEL
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"❌ Error: {str(e)}"

# =========================
# STREAMLIT UI
# =========================
def app():

    st.title("🩺 Diabetes Medical Chatbot")

    try:
        st.image("./images/capsule.png", use_container_width=True)
    except:
        pass

    st.success("Ask only diabetes-related questions.")

    # =========================
    # CHAT HISTORY
    # =========================
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # =========================
    # USER INPUT
    # =========================
    user_query = st.text_input(
        "Ask your diabetes question:"
    )

    # =========================
    # BUTTON
    # =========================
    if st.button("Get Answer"):

        if user_query.strip() == "":
            st.warning("Please enter a question.")

        else:

            with st.spinner("Generating response..."):

                response = ask_gemini(user_query)

                st.session_state.chat_history.append(
                    ("You", user_query)
                )

                st.session_state.chat_history.append(
                    ("Bot", response)
                )

    # =========================
    # DISPLAY CHAT
    # =========================
    st.subheader("Chat History")

    for role, message in st.session_state.chat_history:

        if role == "You":
            st.markdown(f"🧑‍⚕️ **{role}:** {message}")

        else:
            st.markdown(f"🤖 **{role}:** {message}")

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app()