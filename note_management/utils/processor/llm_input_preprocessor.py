import nltk.downloader
import tiktoken
import nltk
from nltk.tokenize import sent_tokenize

def ensure_nltk_data():
    try:
        # Try to use the tokenizer - if it fails, data isn't downloaded
        sent_tokenize("Test sentence.")
    except LookupError:
        # If data isn't downloaded, download it
        nltk.download()

# Ensure NLTK data is available
ensure_nltk_data()

def tokenize_and_split_text(content, max_chunk_size=2500) -> list[str]:
    # Initialize the OpenAI tokenizer (cl100k_base is used by GPT models)
    tokenizer = tiktoken.get_encoding("cl100k_base")
    
    # Split the content into sentences using NLTK's sentence tokenizer
    sentences = sent_tokenize(content)
    
    # Initialize variables to track current chunk size and store chunks
    current_size = 0
    final_chunks = []
    current_chunks = []
    
    # Process each sentence
    for sentence in sentences:
        # Calculate token size of current sentence
        token_size = len(tokenizer.encode(sentence))

        # If adding this sentence won't exceed max_chunk_size, add it to current chunk
        if (current_size + token_size) <= max_chunk_size:
            current_chunks.append(sentence)
            current_size += token_size
        else:
            # If adding would exceed max_chunk_size, save current chunk and start new one
            final_chunks.append(" ".join(current_chunks))
            current_chunks = [sentence]
            current_size = token_size
    
    # Add any remaining sentences as the final chunk
    if current_chunks:
        final_chunks.append(" ".join(current_chunks))
                            
    return final_chunks