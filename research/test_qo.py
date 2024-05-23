import streamlit as st
import openai
import pandas as pd
import os
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader


def process_csv():
    # Load CSV file into a DataFrame
    loader = CSVLoader(os.path.join(os.getcwd(), "data", "cusinfo.csv"))
    df = loader.load()
    return df


def create_chromadb(df):
    # Convert DataFrame to a list of dictionaries
    # data = df.to_dict("records")
    # Initialize ChromaDB and add data
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(df, embeddings)
    return vectorstore


def show():
    st.title("Spaaces Quo with RAG")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chroma_db" not in st.session_state:
        st.session_state.chroma_db = None

    df = process_csv()
    st.session_state.chroma_db = create_chromadb(df)
    st.success("CSV file processed and ChromaDB created")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )
        with st.chat_message("user"):
            st.markdown(prompt)

        if st.session_state.chroma_db is not None:
            retriever = RetrievalQA.from_chain_type(
                llm=openai.Completion,
                chain_type="stuff",
                retriever=st.session_state.chroma_db.as_retriever(),
                return_source_documents=True,
            )
            response = retriever({"query": prompt})
            response_content = response["result"]
            source_documents = response["source_documents"]
            sources = "\n\n".join(
                [f"{i+1}. {doc['text']}" for i, doc in enumerate(source_documents)]
            )
            response_content += f"\n\n**Sources**:\n{sources}"
        else:
            response = openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )
            response_content = response["choices"][0]["message"]["content"]

        with st.chat_message("assistant"):
            st.markdown(response_content)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response_content,
            }
        )


if __name__ == "__main__":
    show()
