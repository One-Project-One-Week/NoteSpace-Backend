import tiktoken

def tokenize_and_split_text(content, max_chunk_size=2500) -> list[str]:
    # Tokenization
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(content)
        
    # Chunking
    tokenized_chunks = [tokens[i:i + max_chunk_size] for i in range(0, len(tokens), max_chunk_size)]
    
    # Decode chunks back to text
    return [tokenizer.decode(chunk) for chunk in tokenized_chunks]