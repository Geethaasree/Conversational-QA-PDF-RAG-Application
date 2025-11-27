## RAG Q&A Conversation With PDF Including Chat History
import os
from typing import List

import streamlit as st
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import requests

from dotenv import load_dotenv
load_dotenv()

hf_token = os.getenv("HF_TOKEN")
if hf_token:
    os.environ['HF_TOKEN']=hf_token
else:
    st.info("Set HF_TOKEN in your .env file to access Hugging Face embeddings.")

embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


## set up Streamlit 
st.title("Conversational RAG With PDF uplaods and chat history")
st.write("Upload Pdf's and chat with their content")

DEFAULT_GROQ_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.1-70b-versatile",
    "llama-3.3-70b-versatile",
    "mixtral-8x22b",
]

def fetch_groq_models(api_key: str) -> List[str]:
    url = "https://api.groq.com/openai/v1/models"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        payload = response.json()
        ids = [item["id"] for item in payload.get("data", []) if item.get("object") == "model"]
        # Prefer deterministic ordering to keep selectbox stable
        ids.sort()
        return ids
    except Exception as exc:
        st.warning(f"Could not load live Groq model list ({exc}). Falling back to defaults.")
        return DEFAULT_GROQ_MODELS

## Input the Groq API Key
api_key=st.text_input("Enter your Groq API key:",type="password")
available_models=DEFAULT_GROQ_MODELS
if api_key:
    live_models=fetch_groq_models(api_key)
    if live_models:
        available_models=live_models

model_name=st.selectbox(
    "Choose a Groq model",
    available_models,
    index=0,
    help="Select any currently supported Groq chat model.",
)

## Check if groq api key is provided
if api_key:
    llm=ChatGroq(groq_api_key=api_key,model_name=model_name)

    ## chat interface

    session_id=st.text_input("Session ID",value="default_session")
    ## statefully manage chat history

    if 'store' not in st.session_state:
        st.session_state.store={}

    uploaded_files=st.file_uploader("Choose A PDf file",type="pdf",accept_multiple_files=True)
    ## Process uploaded  PDF's
    if uploaded_files:
        documents=[]
        for uploaded_file in uploaded_files:
            temppdf=f"./temp.pdf"
            with open(temppdf,"wb") as file:
                file.write(uploaded_file.getvalue())
                file_name=uploaded_file.name

            loader=PyPDFLoader(temppdf)
            docs=loader.load()
            documents.extend(docs)

    # Split and create embeddings for the documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
        splits = text_splitter.split_documents(documents)
        vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
        retriever = vectorstore.as_retriever()    

        contextualize_q_system_prompt=(
            "Given a chat history and the latest user question"
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", contextualize_q_system_prompt),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}"),
                ]
            )
        
        # Answer question
        system_prompt = (
                "You are an assistant for question-answering tasks. "
                "Use the following pieces of retrieved context to answer "
                "the question. If you don't know the answer, say that you "
                "don't know. Use three sentences maximum and keep the "
                "answer concise."
                "\n\n"
                "{context}"
            )
        qa_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}"),
                ]
            )

        # Helper utilities for contextualizing questions and answering with retrieved docs
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs) if docs else ""

        def contextualize_question(question, chat_history):
            if not chat_history:
                return question
            messages = contextualize_q_prompt.format_messages(
                chat_history=chat_history,
                input=question,
            )
            response = llm.invoke(messages)
            return getattr(response, "content", response)

        def answer_with_context(question, docs, chat_history):
            messages = qa_prompt.format_messages(
                chat_history=chat_history,
                input=question,
                context=format_docs(docs),
            )
            response = llm.invoke(messages)
            return getattr(response, "content", response)
        
        def get_session_history(session:str)->BaseChatMessageHistory:
            if session_id not in st.session_state.store:
                st.session_state.store[session_id]=ChatMessageHistory()
            return st.session_state.store[session_id]

        user_input = st.text_input("Your question:")
        if user_input:
            session_history=get_session_history(session_id)
            standalone_question=contextualize_question(user_input, session_history.messages)
            retrieved_docs=retriever.invoke(standalone_question)
            answer=answer_with_context(user_input, retrieved_docs, session_history.messages)
            session_history.add_user_message(user_input)
            session_history.add_ai_message(answer)
            st.write(st.session_state.store)
            st.write("Assistant:", answer)
            st.write("Chat History:", session_history.messages)
else:
    st.warning("Please enter the GRoq API Key")










