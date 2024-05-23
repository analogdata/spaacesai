import streamlit as st
import pandas as pd
from langchain.chains import create_retrieval_chain, LLMChain
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import PromptTemplate
import os

# Load your data
df = pd.read_csv(os.path.join(os.getcwd(), "data", "cusinfo.csv"))

# Initialize ChromaDB
vector_store = Chroma.from_pandas(df, embedding_key="your_embedding_key")

# Create a retriever
retriever = vector_store.as_retriever()

# Initialize OpenAI LLM
llm = OpenAI(api_key="your-openai-api-key")

# Create a prompt template for question generation
template = (
    "Combine the chat history and follow up question into "
    "a standalone question. Chat History: {chat_history}\n"
    "Follow up question: {question}"
)
prompt = PromptTemplate.from_template(template)
question_generator_chain = LLMChain(llm=llm, prompt=prompt)

# Combine retrieved documents
combine_docs_chain = create_stuff_documents_chain(llm, prompt)

# Create the retrieval chain
chain = create_retrieval_chain(
    retriever=retriever,
    question_generator=question_generator_chain,
    combine_docs_chain=combine_docs_chain,
)

# Streamlit application
st.title("Langchain and ChromaDB Streamlit App")

# Display the dataframe
st.write("Customer Information Data:")
st.dataframe(df)

# Input for user query
user_query = st.text_input("Enter your query:")

# Collect chat history (optional)
chat_history = st.session_state.get("chat_history", [])

# Process the query with Langchain
if user_query:
    response = chain.invoke({"input": user_query, "chat_history": chat_history})
    chat_history.append({"role": "user", "content": user_query})
    chat_history.append({"role": "assistant", "content": response["answer"]})
    st.write("Response:")
    st.write(response["answer"])

# Save chat history
st.session_state["chat_history"] = chat_history
