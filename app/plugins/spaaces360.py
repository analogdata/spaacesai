import os
import streamlit as st

from langchain.llms import OpenAI
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.chains import RetrievalQA

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings


# llm = OpenAI(temperature=0.7)
# embeddings = OpenAIEmbeddings()

# loader = CSVLoader(os.path.join(os.getcwd(), "data", "cusinfo.csv"))

# doc_data = loader.load()

# vectorstore = Chroma.from_documents(doc_data, embeddings)


def show():
    st.title("Spaaces 360")

    # chain = RetrievalQA.from_chain_type(
    #     llm=llm,
    #     chain_type="stuff",
    #     retriever=vectorstore.as_retriever(),
    #     input_key="question",
    #     return_source_documents=True,
    # )

    # query = st.text_input("Question")

    # st.write(
    #     chain(
    #         {"question": query},
    #     )
    # )
