import streamlit as st
from utils.summarizer import summarize_text, extract_text_from_pdf
from utils.grammar_checker import correct_grammar

def show_home():
    st.title("🛠️ WordSmith")
    st.subheader("Use these Tools to enhance your writing.")

    # Custom CSS for cards
    st.markdown("""
        <style>
        .card {
            border-radius: 15px;
            padding: 30px 20px;
            background: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 10px 0;
            transition: all 0.3s ease;
            border: 1px solid #f0f0f0;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
        }
        .card-icon {
            font-size: 40px;
            margin-bottom: 15px;
            color: #0083B8;
        }
        .card-title {
            color: #0083B8;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .card-description {
            color: #666;
            font-size: 16px;
            margin-bottom: 20px;
        }
        .custom-button {
            background-color: #0083B8;
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            font-weight: 500;
            transition: background-color 0.3s ease;
            width: 100%;
            max-width: 200px;
        }
        .custom-button:hover {
            background-color: #006491;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="card">
                <div class="card-icon">📝</div>
                <div class="card-title">Summarizer Tool</div>
                <div class="card-description">
                    Summarize your text or PDF using this tool. Perfect for research, content analysis, 
                    and quick document review.
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Click to Use", key="sum_btn", use_container_width=True):
            st.session_state.page = "summarizer"
            st.rerun()

    with col2:
        st.markdown("""
            <div class="card">
                <div class="card-icon">✍️</div>
                <div class="card-title">Grammar Corrector Tool</div>
                <div class="card-description">
                    Enhance your writing with this grammar correction tool. 
                    Get instant fixed sentences or words by AI.
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Click to Use", key="gram_btn", use_container_width=True):
            st.session_state.page = "grammar"
            st.rerun()

def show_summarizer():
    st.title("📝 Text Summarization")
    
    if st.button("← Back to Home", type="secondary"):
        st.session_state.page = "home"
        st.rerun()
    
    input_method = st.radio("Choose input method:", ["Text Input", "PDF Upload"])
    target_ratio = st.slider("Summary Retention Ratio (%)", min_value=10, max_value=50, value=30) / 100
    
    if input_method == "Text Input":
        text_input = st.text_area("Enter your text below", height=300)
        if st.button("Summarize Text"):
            if text_input.strip():
                st.subheader("Summarized Text:")
                try:
                   summary = summarize_text(text_input, target_ratio=target_ratio)
                   st.write(summary)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.warning("Please enter text to summarize.")
    else:
        uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
        if st.button("Summarize PDF"):
            if uploaded_file is not None:
                try:
                    extracted_text = extract_text_from_pdf(uploaded_file)
                    summary = summarize_text(extracted_text, target_ratio=target_ratio)
                    st.subheader("Summarized Text:")
                    st.write(summary)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.warning("Please upload a PDF file.")

def show_grammar_checker():
    st.title("✍️ Grammar Correction")
    
    if st.button("← Back to Home", type="secondary"):
        st.session_state.page = "home"
        st.rerun()
    text_input_grammar = st.text_area("Enter text for grammar correction", height=300)
    if st.button("Correct Grammar"):
        if text_input_grammar.strip():
            st.subheader("Corrected Text:")
            try:
                corrected_text = correct_grammar(text_input_grammar)
                st.write(corrected_text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter text to correct.")

def main():
    st.set_page_config(
        page_title="AI-Text Tools",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state for navigation
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    
    # Page routing
    if st.session_state.page == "home":
        show_home()
    elif st.session_state.page == "summarizer":
        show_summarizer()
    elif st.session_state.page == "grammar":
        show_grammar_checker()

if __name__ == "__main__":
    main()
