# requires the `transformers` package; please install with `pip -U install transformers`

import sys
from transformers import GPT2Tokenizer

def count_tokens(file_path):
    print(f"Counting the token count estimate for: {inputfile} ...", flush=True)
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:            
            text = file.read()
            tokens = tokenizer.encode(text)
            return len(tokens)
    except Exception as e:
        print(f"Error processing file: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: tokencounter.py <inputfile>")
        sys.exit(1)

    inputfile = sys.argv[1]
    token_count = count_tokens(inputfile)

    if token_count is not None:
        print(f"Estimated token count: {token_count}")