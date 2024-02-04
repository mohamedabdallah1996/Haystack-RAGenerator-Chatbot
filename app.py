from haystack.nodes import PreProcessor, AnswerParser, PromptNode, PromptTemplate, BM25Retriever, TransformersSummarizer
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import PDFToTextConverter
from haystack import Pipeline
from pathlib import Path

from settings import HF_API_KEY
from pprint import pprint

import chainlit as cl

# PDF to text converter initialization
converter = PDFToTextConverter(
    remove_numeric_tables=True,
    valid_languages=["en"]
)
# Conversion of the PDF document to text
docs = converter.convert(file_path=Path("data/Employee-Handbook.pdf"), meta=None)

# Pre-processing of the documents
preprocessor = PreProcessor(
    clean_empty_lines=True,
    clean_whitespace=False,
    clean_header_footer=True,
    split_by="word",
    split_length=300,
    split_respect_sentence_boundary=True,
)

preprocessed_docs = preprocessor.process(docs)

# In-memory document store initialization and document writing
document_store = InMemoryDocumentStore(use_bm25=True)
document_store.write_documents(preprocessed_docs)

# BM25 retriever initialization
retriever = BM25Retriever(document_store=document_store, top_k=3)

# Prompt template for question-answering
prompt_template = PromptTemplate(
    prompt="""
    Answer the question truthfully based solely on the given documents. If the documents do not contain the answer to the question, say that answering is not possible given the available information. Your answer should be no longer than 50 words.
    Documents:{join(documents)}
    Question:{query}
    Answer:
    """,
    output_parser=AnswerParser(),
)

# Prompt node initialization for handling prompts
prompt_node = PromptNode(
    model_name_or_path="mistralai/Mistral-7B-Instruct-v0.1",
    api_key=HF_API_KEY,
    default_prompt_template=prompt_template
)

# Summarizer initialization using Transformers
summarizer = TransformersSummarizer(model_name_or_path="google/pegasus-xsum")

# Definition of the entire pipeline
rag_pipeline = Pipeline()
rag_pipeline.add_node(component=retriever, name="retriever", inputs=["Query"])
rag_pipeline.add_node(component=prompt_node, name="prompt_node", inputs=["retriever"])
rag_pipeline.add_node(component=summarizer, name="Summarizer", inputs=["prompt_node"])
rag_pipeline.add_node(component=document_store, name="DocumentStore", inputs=["Summarizer"])

print_answer = lambda answer: pprint(answer['answers'][0].answer.strip())

print_answer(rag_pipeline.run(query="what is the recruitment and selection process?", 
                              params = {"debug": True, "retriever": {"top_k": 1}, "prompt_node": {"debug": True}}))

@cl.on_message
async def main(message: str):
    response = await cl.make_async(rag_pipeline.run)(message)
    sentences = response['answers'][0].answer.split('\n')

    # Check if the last sentence doesn't end with '.', '?', or '!'
    if sentences and not sentences[-1].strip().endswith(('.', '?', '!')):
        # Remove the last sentence
        sentences.pop()

    result = '\n'.join(sentences[1:])
    await cl.Message(author="Bot", content=result).send()

