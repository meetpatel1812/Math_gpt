import streamlit as st
from groq import Groq

st.markdown(hide_github_icon, unsafe_allow_html=True)
st.set_page_config(page_icon="💬", page_title="Math GPT by Meet Patel")
hide_github_icon = """
#GithubIcon {
  visibility: hidden;
}
"""
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
# Sidebar for API key input and model selection
with st.sidebar:
    st.title("Select Model")
    
    
    # Model selection
    models = {
        "gemma-7b-it": {"name": "Gemma-7b-it", "tokens": 8192, "developer": "Google"},
        "llama3-70b-8192": {"name": "LLaMA3-70b-8192", "tokens": 8192, "developer": "Meta"},
        "llama3-8b-8192": {"name": "LLaMA3-8b-8192", "tokens": 8192, "developer": "Meta"},
        "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
    }
    
    selected_model = st.selectbox("Select Model", options=list(models.keys()), format_func=lambda key: models[key]["name"])

    "[LinkedIn](https://www.linkedin.com/in/meetpatel1812/)"
    

# Title and description
st.subheader("🅜 Math GPT by Meet",divider="red", anchor=False)


# Initialize message history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you with your math problem today?"}
    ]

# Separate system message for controlling chatbot behavior
system_message = {
    "role": "system",
    "content": "You are a mathematical GPT. You only respond to mathematical queries and politely decline to answer any non-mathematical questions."
}

# Display chat history excluding the system message
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input handling
if prompt := st.chat_input():
    if not client:
        st.info("Please add your Groq API key to continue.")
        st.stop()

    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Groq API call with system message and selected model
    try:
        response = client.chat.completions.create(
            model=selected_model,  # Use the model selected by the user
            messages=[system_message] + st.session_state.messages  # Include system message only in the API call
        )
        msg = response.choices[0].message.content
    except Exception as e:
        msg = f"An error occurred: {str(e)}"
    
    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
