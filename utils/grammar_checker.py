from happytransformer import HappyTextToText, TTSettings

# Initialize the HappyTextToText object
happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")

# Configure settings for generation
args = TTSettings(num_beams=5, min_length=1)

def correct_grammar(text):
    """
    Corrects grammar using the HappyTransformer library with a T5 fine-tuned model.
    """
    # Prefix "grammar: " is required for the fine-tuned model
    input_text = f"grammar: {text}"
    
    # Generate the corrected text
    result = happy_tt.generate_text(input_text, args=args)
    
    return result.text

