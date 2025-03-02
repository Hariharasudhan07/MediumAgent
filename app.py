import os
import streamlit as st
from dotenv import load_dotenv
from fpdf import FPDF
from io import BytesIO
from docx import Document
from googlesearchagent import NewsSearchAgent
from webscrapagent import WebSearchAgent
from agno.agent import Agent
from agno.models.google import Gemini


def load_api_key():
    """Load and return the Gemini API key from environment variables."""
    load_dotenv()
    return os.getenv('geminiapi')

def get_search_results(user_query):
    """Search for articles related to the user query using NewsSearchAgent."""
    news_agent = NewsSearchAgent()
    results = news_agent.run(user_query)
    return results

def build_data_store(results):
    """For each result URL, fetch its summary using WebSearchAgent and build a data store."""
    web_agent = WebSearchAgent()
    data_store = []
    progress_bar = st.progress(0)
    for i, url in enumerate(results, start=1):
        st.write(f"### Processing URL {i}/{len(results)}")
        with st.expander(f"🔗 {url}"):
            summary = web_agent.search_webpage(url)
            st.write(summary)
            data_store.append({"url": url, "summary": summary})
        progress_bar.progress(i / len(results))
    return data_store

def generate_blog(data_store, apikey):
    """Generate a blog post using the retrieved data_store via an AGNO RAG agent."""
    rag_agent = Agent(
        name="RAG Blog Agent",
        agent_id="rag-agent",
        model=Gemini(id="gemini-2.0-flash-exp", api_key=apikey),
        read_chat_history=True,
        instructions=[
            "Use only the retrieved documents to generate content.",
            "Ensure the blog is structured concisely with headings.",
            "Write in a natural, humanized style without excessive bullet points.",
            "Use tables where appropriate to present structured information.",
            "Include relevant code snippets when necessary.",
            "Provide references if applicable.",
            "Incorporate images where relevant to enhance understanding.",
            "Use examples, statistics, quotes, and diagrams where necessary.",
        ],
        markdown=True,
    )
    prompt = f"""You are a professional blogger. Write a concise, engaging, and structured blog using the information below.

### Information:
{data_store}

### Blog:
"""
    # Remove streaming so that the output is returned in one go.
    return rag_agent.run(prompt)

def save_as_markdown(blog_output):
    md_content = blog_output.encode("utf-8")
    return md_content




def save_as_pdf(blog_output):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    try:
        # Use a built-in font (Arial) to avoid issues
        pdf.set_font("Arial", size=12)
        
        # Add content
        pdf.multi_cell(0, 10, blog_output)

        # Save PDF to a BytesIO object
        pdf_stream = BytesIO()
        pdf.output(pdf_stream, "F")
        pdf_stream.seek(0)

        return pdf_stream.getvalue()  # Return bytes instead of None

    except Exception as e:
        st.error(f"PDF generation error: {e}")
        return b""  # Return empty bytes instead of None



def save_as_word(blog_output):
    doc = Document()
    doc.add_paragraph(blog_output)
    
    word_stream = BytesIO()
    doc.save(word_stream)
    word_stream.seek(0)
    
    return word_stream.getvalue()


# Streamlit App configuration
st.set_page_config(page_title="Blog Generator", page_icon="📝", layout="wide")
st.title("📝 Automated Blog Generator with AGNO RAG")

apikey = load_api_key()
user_query = st.text_input("🔍 Enter a topic to search for:", placeholder="e.g., Artificial Intelligence Trends")

if st.button("🚀 Generate Blog", use_container_width=True):
    if not user_query:
        st.error("⚠️ Please enter a topic to search for.")
    else:
        with st.spinner("Fetching news articles..."):
            results = get_search_results(user_query)
        
        if results:
            st.success(f"✅ Found {len(results)} articles.")
            st.subheader("🔗 Found URLs:")
            for url in results:
                st.markdown(f"- [{url}]({url})")
            
            with st.spinner("Summarizing articles..."):
                data_store = build_data_store(results)
            st.success("📄 Summaries retrieved successfully.")

            with st.spinner("📝 Generating blog..."):
                blog_response = generate_blog(data_store, apikey)
                # Extract string content from the response
                blog_output = blog_response.content if hasattr(blog_response, "content") else str(blog_response)
            
            st.success("🎉 Blog generated successfully!")
            st.markdown(blog_output, unsafe_allow_html=True)
            
            st.subheader("📜 Download Blog:")
            md_file = save_as_markdown(blog_output)
            pdf_file = save_as_pdf(blog_output)
            docx_file = save_as_word(blog_output)
            
            st.download_button("📥 Download as Markdown", save_as_markdown(blog_output), file_name="generated_blog.md")
            st.download_button("📥 Download as Word", save_as_word(blog_output), file_name="generated_blog.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            st.download_button("📥 Download as PDF",save_as_pdf(blog_output),file_name="generated_blog.pdf",mime="application/pdf")

        else:
            st.error("❌ No articles found. Please try a different query.")
 