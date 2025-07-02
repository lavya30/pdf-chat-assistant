import os
import streamlit as st
from dotenv import load_dotenv

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# Load environment variables
load_dotenv()

# Set GROQ API key
groq_api_key = os.getenv("GROQ_API_KEY") 

# Initialize LLM
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model="meta-llama/llama-4-scout-17b-16e-instruct"
)

# Prompt setup
prompt = ChatPromptTemplate.from_template("""
You are a helpful and precise business analyst.

Answer the question based only on the provided document context.
If you cannot find the answer in the context, respond with:
"I could not find specific information on that topic in the document."

<context>
{context}
</context>

Question: {input}
Answer:
""")

# Streamlit UI
st.set_page_config(page_title="Executive Summary Generator")
st.title("Executive Summary Generator")

# File uploader
uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])

# Processing only if a file is uploaded and new
if uploaded_pdf is not None:
    if "last_uploaded_file_name" not in st.session_state or uploaded_pdf.name != st.session_state.last_uploaded_file_name:
        with st.spinner("Processing uploaded PDF..."):
            try:
                # Save file
                temp_path = "temp_uploaded.pdf"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_pdf.read())

                # Load and split
                loader = PyPDFLoader(temp_path)
                docs = loader.load()

                splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                chunks = splitter.split_documents(docs)

                # Embed and create vectorstore
                embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
                vectorstore = FAISS.from_documents(chunks, embeddings)

                # Store in session
                st.session_state.vectorstore = vectorstore
                st.session_state.last_uploaded_file_name = uploaded_pdf.name

                st.success("✅ PDF processed. You can now ask questions.")

            except Exception as e:
                st.error("❌ PDF processing failed.")
                st.exception(e)

# Question box (after PDF is processed)
if "vectorstore" in st.session_state:
    user_query = st.text_input("Enter your question (e.g., 'Give an executive summary')")
    if st.button("📄 Generate Summary") and user_query.strip():
        try:
            retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 10})
            doc_chain = create_stuff_documents_chain(llm, prompt)
            retrieval_chain = create_retrieval_chain(retriever, doc_chain)

            response = retrieval_chain.invoke({"input": user_query})
            st.markdown("### 📬 Answer:")
            st.write(response['answer'])

        except Exception as e:
            st.error("❌ LLM failed to generate a response.")
            st.exception(e)
