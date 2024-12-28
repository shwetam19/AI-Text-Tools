from transformers import pipeline
import PyPDF2
import re

def clean_text(text):
    """
    Cleans the input text by removing non-standard characters and excessive newlines.
    """
    text = re.sub(r'\s+', ' ', text)  # Remove excessive whitespace
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
    return text.strip()

def split_text_into_chunks(text, chunk_size=300):
    """
    Splits the input text into chunks of a specified size.
    """
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def summarize_text(text, target_ratio=0.3, re_summarize=True):
    """
    Summarizes the input text to retain the desired ratio of content (e.g., 30%).
    Handles short and long texts with chunking and optional re-summarization.
    """
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Log the input text length
    word_count = len(text.split())
    print(f"Input text length: {word_count} words")

    # Handle short texts directly
    if word_count <= 200:  # Threshold for "short" texts
        print("Short text detected, adjusting summarization parameters.")
        try:
            max_length = max(100, int(word_count * target_ratio))  # At least 30% of input
            min_length = max(50, int(word_count * target_ratio * 0.5))  # Half of max length
            print(f"Short text summarization parameters: max_length={max_length}, min_length={min_length}")
            summary = summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            return summary[0]['summary_text']
        except Exception as e:
            return f"Error summarizing short text: {e}"

    # Handle longer texts with chunking
    chunks = split_text_into_chunks(text, chunk_size=300)
    print(f"Number of chunks created: {len(chunks)}")

    summaries = []
    for i, chunk in enumerate(chunks):
        input_length = len(chunk.split())
        max_length = max(50, int(input_length * target_ratio))
        min_length = max(30, int(input_length * target_ratio * 0.5))

        try:
            summary = summarizer(
                chunk,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            summaries.append(summary[0]['summary_text'])
            print(f"Chunk {i + 1} summary: {summary[0]['summary_text']}")
        except Exception as e:
            summaries.append(f"Error summarizing chunk {i + 1}: {e}")
            print(f"Error summarizing chunk {i + 1}: {e}")

    # Combine all summaries
    combined_summary = ' '.join(summaries)
    print(f"Combined summary length: {len(combined_summary.split())} words")

    # Optionally re-summarize the combined summary
    combined_summary_length = len(combined_summary.split())
    if re_summarize and combined_summary_length > 50:
        print("Re-summarizing the combined summary for coherence...")
        try:
            max_length = max(50, int(combined_summary_length * target_ratio))
            min_length = max(20, int(combined_summary_length * target_ratio * 0.5))

            # Avoid setting max_length greater than input length
            if max_length >= combined_summary_length:
                max_length = combined_summary_length - 1

            final_summary = summarizer(
                combined_summary,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            print(f"Final summary length: {len(final_summary[0]['summary_text'].split())} words")
            return final_summary[0]['summary_text']
        except Exception as e:
            return f"Error during re-summarization: {e}"

    # Skip re-summarization for very short combined summaries
    print("Skipping re-summarization as the combined summary is already concise.")
    return combined_summary


def extract_text_from_pdf(file):
    """
    Extracts and cleans text from an uploaded PDF file.
    """
    pdf_reader = PyPDF2.PdfReader(file)
    extracted_text = ""

    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            extracted_text += page_text + "\n"

    if not extracted_text.strip():
        raise ValueError("The PDF does not contain extractable text.")

    return clean_text(extracted_text)
