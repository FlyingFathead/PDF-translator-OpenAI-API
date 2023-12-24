# PDF-translator-OpenAI-API
Experimental Python-based PDF/plaintext translator that utilizes the OpenAI API

- **NOTE: this is a highly experimental and WIP pipeline for dumping PDF's into plaintext and getting them translated through the OpenAI API**
- **I do NOT recommend running it without first studying the code since it's very much just a preliminary draft**

# Prerequisites
- `pdfmine.py` requires `pdfminer.six` -- install with: `pip install -U pdfminer.six`
- `tokencounter.py` requires `transformers` -- install with `pip install -U transformers`
- Translation module requires the `openai` package (`pip install -U openai`) and a functioning API key.
- Put the API key into your environmental variables or as `api_token.txt` into your program directory.

# Functionalities so far
- Use `pdfmine.py your_file.pdf` to dump the text layer of a PDF to plaintext.
- Use `tokencounter.py` to estimate the amount of tokens that the text file has for a rough token usage estimate.
- Use `splitter.py textfile.txt` to split the text file into pieces that are more suitable for LLM's such as GPT-3.5 or GPT-4. It splits at 5000 chars at newline by default, but can be adjusted from the `char_limit` variable. The `splitter.py` also tries to auto-sanitize tha pdf dump at the moment -- this might not be suitable for your use case scenario, so again -- look at the split dumps first before you run it through a LLM translation -- GIGO (garbage in, garbage out) applies to NLP translations as well.
- (Coming soon) pipeline to automate the actual translation process.

# Todo
- Looking into PDF file layers to see if we could replace the contents in-place (get text block layer from PDF page => sanitize => LLM translate => insert back in-place)
