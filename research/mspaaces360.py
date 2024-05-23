import os
import streamlit as st
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA


loader = CSVLoader(os.path.join(os.getcwd(), "cusinfo.csv"))
data = loader.load()

llm = OpenAI(temperature=0.7)
embeddings = OpenAIEmbeddings()

vectorstore = FAISS.from_documents(data, embeddings)

st.title("Modern Spaaces 360")

# def generate_response(input_text):
llm = OpenAI(temperature=0.7)

chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(),
)


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

if "messages" not in st.session_state:
    st.session_state.messages = []

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

    response = chain.invoke(str(prompt))
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response["result"],
        }
    )

    with st.chat_message("assistant"):
        st.markdown(response["result"])
