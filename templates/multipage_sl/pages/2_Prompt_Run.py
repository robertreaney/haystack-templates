import streamlit as st
from pipelines import RAG
import streamlit as st

st.title('Execute a Prompt')

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


# folder = st.file_uploader("Select a folder:", type="folder")
# if folder is not None:
#     folder_path = folder.name
#     st.write("Selected folder:", folder_path)

# Dropdown list options
selected_question = st.selectbox("Select a question:", [
    "Summarize Robert Reaney's accomplishments.",
    "Give me all the candidates qualified to teach."
])

# Button to trigger chatbot response
if st.button("Get Chatbot Response"):
    response = get_chatbot_response(selected_question)
    st.write(response)
