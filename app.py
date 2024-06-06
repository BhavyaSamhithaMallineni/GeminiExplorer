
from urllib import response
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, ChatSession
import vertexai
from google.cloud import aiplatform

# Initialize the Vertex AI with the project ID
project = "gemini-explorer-424915"
vertexai.init(project=project)

# Configure the generative model
config = generative_models.GenerationConfig(temperature=0.4)
model = GenerativeModel("gemini-pro")

# Initialize Streamlit layout
st.title("Gemini Explorer")


# Initialize message history in session state if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

def llm_function(chat: ChatSession, query, display_user=True, display_model=True):
    # Send message to the model and receive the response
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    # Append messages to session state
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "model", "content": output})

    # Display user and model messages only based on the display flags
    if display_user:
        with st.chat_message("user"):
            st.markdown(query)
    
    if display_model:
        with st.chat_message("model"):
            st.markdown(output)


# Start a chat session with the generative model
chat = model.start_chat()
st.write("## My First App")
# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capture user input
query = st.chat_input("Ask Gemini Flights")

# Process the input if provided
if query:
    llm_function(chat, query)

if len(st.session_state.messages) == 0:
    initial_prompt = "Introduce yourself as ReX_Intelligent and say Hi to the person asking using the above response, an assistant powered by Google Gemini. Start the conversation by a riddle and use emojis in the response"
    llm_function(chat, initial_prompt, display_user=False, display_model=True)
