import streamlit as st
import yaml
from llm_bot import dummy_bot, echo_bot #contains logic for bot's response

# Own imports
from constants import EXAMPLE_QUESTIONS, SYSTEM_PROMPT

def clear_chat_history() -> None:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state.example_question = ""
    st.session_state.user_prompts = ["",]

# Read config yaml file
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)
#print(config)
title = config['streamlit']['title']
avatar = {
    'user': None,
    'assistant': config['streamlit']['avatar']
}

# Set page config
st.set_page_config(
    page_title=config['streamlit']['tab_title'], 
    page_icon=config['streamlit']['page_icon'], 
    layout="wide"
    )

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}] 

if "display" not in st.session_state:
    st.session_state.display =  []

if "user_prompts" not in st.session_state:
    st.session_state.user_prompts = ["",]

# Set sidebar
st.sidebar.title("About")
st.sidebar.info(config['streamlit']['about'])

example_prompt: str = st.sidebar.selectbox(label="Example Questions", options=EXAMPLE_QUESTIONS, key="example_question")
st.session_state.user_prompts.append(example_prompt)

st.markdown("""
    <style>
    .no-padding-margin-border {
        padding-top: 0 !important;
        margin-top: 0 !important;
        border-top: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

logo_slot, title_slot = st.columns([.6, 20])  # Adjust the ratio as needed

# Add a logo in the first column
with logo_slot:
    st.image(config['streamlit']['logo'], width=37)  # Adjust the width as needed

# Add the title in the second column
with title_slot:
    st.markdown(f'<h1 class="no-padding-margin-border">{title}</h1>', unsafe_allow_html=True)




# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] in ["user", "assistant"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if input_prompt:= st.chat_input("Send a message"):
    st.session_state.user_prompts.append(input_prompt)
# React to user input
if st.session_state.user_prompts[-1]:
    prompt = st.session_state.user_prompts[-1]
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = echo_bot(prompt) 
            st.markdown(response) 
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)


st.markdown("""
    <style>
    .stButton > button {
        background-color: transparent;
        border: none;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)
st._bottom.button("🧹 **Clear Chat History**",  on_click=clear_chat_history, use_container_width=True)
    
