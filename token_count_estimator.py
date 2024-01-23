# token_count_estimator.py
#
# use this utility to get a rough estimate on your total token counts in your project
#
# note that counting tokens on i.e. a database dump (megabytes, tens of megabytes, etc in size)
# is a time and cpu-consuming task. even with `concurrent.futures`, it can take a while to do the
# overall token counts if your text dump is very large.

import shutil
import sys
import spacy
import concurrent.futures
from transformers import GPT2Tokenizer

# Set the spaCy model here
SPACY_MODEL = "fi_core_news_sm"  # Finnish model
# SPACY_MODEL = "en_core_web_sm"  # English model

# for fi model, use:
# python -m spacy download fi_core_news_sm

# print term width horizontal line
def hz_line(character='-'):
    terminal_width = shutil.get_terminal_size().columns
    line = character * terminal_width
    print(line)
    sys.stdout.flush()  # Flush the output to the terminal immediately

def count_tokens_spacy_chunk(chunk):
    nlp = spacy.load(SPACY_MODEL)  
    doc = nlp(chunk)
    return len(doc)

def count_tokens_spacy(text, chunk_size=1000000, max_workers=5):
    nlp = spacy.load(SPACY_MODEL)
    print(f"Using spaCy model: {SPACY_MODEL}")
    nlp.max_length = chunk_size
    token_count = 0

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(count_tokens_spacy_chunk, text[start:start + chunk_size])
                   for start in range(0, len(text), chunk_size)]
        for future in concurrent.futures.as_completed(futures):
            token_count += future.result()

    return token_count

def count_tokens_huggingface(text):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    return len(tokenizer.encode(text))

def main(file_path):
    hz_line()
    print(f"Counting tokens, please wait. This will either take a while or a longer while, depending on your file size.", flush=True)
    hz_line()
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    spacy_count = count_tokens_spacy(text)
    hf_count = count_tokens_huggingface(text)

    print(f"spaCy Token Count: {spacy_count}")
    print(f"Hugging Face Token Count: {hf_count}")
    hz_line()
    print(f"Please note that the mentioned figures are only intended to give you a rough estimate on the token countes.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python token_count_estimator.py <file_path>")
        sys.exit(1)

    main(sys.argv[1])