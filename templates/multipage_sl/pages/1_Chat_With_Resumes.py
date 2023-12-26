import streamlit as st

from pipelines import RAG

st.set_page_config(page_title='Resume Chatbot', page_icon=':robot_face:')

# Streamlit app
template = """
Given the following resume information, answer the question about the job applicants.

Context:
{% for document in documents %}
    {{ document.content }}
{% endfor %}

Question: {{question}}
Answer:
"""
pipeline = RAG(directory='documents', template=template)

# Function to simulate chatbot response (In real application, replace this with actual chatbot logic)
def get_chatbot_response(question):
    response = pipeline.run({"retriever": {"query": question}, "prompt_builder": {"question": question}})
    return f'{response["llm"]["replies"][0]}'  # Echoes the user message for demonstration

st.title("Resume Chatbot")

# prompt = st.chat_input('Say something')

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if prompt := st.chat_input("Say something"):
    # display user message
    with st.chat_message('user'):
        st.markdown(prompt)
    # add user message to history
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    response = get_chatbot_response(prompt)
    with st.chat_message('assistant'):
        st.markdown(response)

    st.session_state.messages.append({'role': 'assistant', 'content': response})
