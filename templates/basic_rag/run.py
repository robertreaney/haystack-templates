from haystack.telemetry import tutorial_running
from haystack.document_stores import InMemoryDocumentStore
from haystack.components.converters import PyPDFToDocument
from haystack.components.retrievers import InMemoryBM25Retriever
from haystack.components.builders import PromptBuilder
from haystack.components.generators import GPTGenerator
from haystack.pipeline import Pipeline

from haystack import Document
import os
from pathlib import Path

# submit telemetry
# tutorial_running(27)

def init():
    # initialize document store
    document_store = InMemoryDocumentStore()

    # read pdfs with converter
    converter = PyPDFToDocument()
    results = converter.run(sources=list(Path('documents').rglob('*.pdf')))
    docs = [Document(content=doc.content, meta=doc.meta) for doc in results["documents"]]

    # load docs into store
    document_store.write_documents(docs)

    # init retreiver
    retriever = InMemoryBM25Retriever(document_store)

    # define the prompt
    template = """
    Given the following resume information, answer the question about the job applicants.

    Context:
    {% for document in documents %}
        {{ document.content }}
    {% endfor %}

    Question: {{question}}
    Answer:
    """

    prompt_builder = PromptBuilder(template=template)

    # initialize generator
    openai_api_key = os.getenv("OPENAI_API_KEY", None)
    generator = GPTGenerator(api_key=openai_api_key)

    # build the pipeline
    basic_rag_pipeline = Pipeline()
    # Add components to your pipeline
    basic_rag_pipeline.add_component("retriever", retriever)
    basic_rag_pipeline.add_component("prompt_builder", prompt_builder)
    basic_rag_pipeline.add_component("llm", generator)

    # Now, connect the components to each other
    basic_rag_pipeline.connect("retriever", "prompt_builder.documents")
    basic_rag_pipeline.connect("prompt_builder", "llm")
    return basic_rag_pipeline

    # basic_rag_pipeline.draw("./templates/barebones/basic-rag-pipeline.png")

    # as a question
    # question = "Reccomend a candidate to hire for a Data Scientist position. Only give me the name of the candidate with no justification."

    # response = basic_rag_pipeline.run({"retriever": {"query": question}, "prompt_builder": {"question": question}})

    # print(response["llm"]["replies"][0])

