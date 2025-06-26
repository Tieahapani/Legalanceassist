import streamlit as st
from access_agent import search_with_gemini
from explain import simplify_with_claude

# Set up Streamlit page
st.set_page_config(page_title="Legalance", page_icon="🕵️", layout="centered")

# 🔷 Custom styled title with emoji and capital 'L'
st.markdown(""" 
     <style>
        .stApp {
            background-color: #f0f8ff;
        }
    </style>
    <h1 style='text-align: center; font-size: 48px;'>
        🕵️ <span style="color:#4B8BBE;">Legalance</span>
    </h1>
    <p style='text-align: center; font-size:18px;'>
        Your friendly multilingual immigration assistant
    </p>
    <hr>
""", unsafe_allow_html=True)

# 🔁 Initialize chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []


# 💬 Display chat history (role-based)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"🧑 **You:** {msg['text']}")
    else:
        st.markdown(f"🤖 **Legalance:** {msg['text']}")
        
        if "link" in msg and msg["link"]:
            st.markdown(f"🔗 [Source]({msg['link']})", unsafe_allow_html=True)    

# 📝 User input
user_input = st.text_input("Ask your immigration or visa questions:")

language = st.selectbox( 
    "Choose output language:",
    ["English", "Hindi", "Spanish", "French", "Bengali", "Tamil", "Telugu"]
)

# 🔘 Ask button
if st.button("Ask"):
    if user_input.strip():
        # Store user message
        st.session_state.messages.append({"role": "user", "text": user_input})

        # Process the question
        with st.spinner("Legalance is thinking..."):
            gemini_response, source_link = search_with_gemini(user_input)
            answer = simplify_with_claude(gemini_response, target_language=language.lower())

        # Store bot response
        st.session_state.messages.append({"role": "bot", "text": answer, "link": source_link})

        # Rerun the app to show updated chat
        st.rerun()