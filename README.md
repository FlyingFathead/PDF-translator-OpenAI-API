# PDF-translator-OpenAI-API
Experimental Python-based PDF/plaintext translator that utilizes the OpenAI API

- **NOTE: this is a highly experimental WIP pipeline for dumping PDF's into plaintext and getting them translated through the OpenAI API.**

- **I do NOT recommend running it without first studying the code since the program is just an early trial at this point.**

# Prerequisites
- Text extraction from PDF files requires `pdfminer.six` -- install with: `pip install -U pdfminer.six`
- Token counting (to calculate estimated API costs) requires `transformers` -- install with `pip install -U transformers`
- Translation module when using OpenAI API requires the `openai` package (`pip install -U openai`) and a functioning OpenAI API key.
- Put the OpenAI API key into your environmental variables as `OPENAI_API_KEY` or into a single line entry into `api_token.txt` in the program directory.

# Functionalities so far / processing order

0/x) `pdfget.py <directory>` will use `fitz` (PyMuPDF) in order to dump the text in a natural reading order by approximating the position on the page.
1) `pdf_reader_splitter.py <pdf file>` to dump to splits by page straight from the pdf. Also supports cmdline option for setting split on chars. WIP, as usual.
2) `openai_api_auto_translate.py <directory name>` to translate an entire directory (where you dumped your stuff into with `pdf_reader_splitter.py`). Edit `config.ini` to set your own parameters for translation.
3) `combine_translation.py <directory name>` to combine the splits back into one piece.
4) `post_process.py <textfile>` for final touches, i.e. any paragraphs that are without an empty line in between, add one in, and trim multiple empty lines.

# WIP
- `gui-translator.py` - an early alpha GUI for side-by-side / A/B type comparison with a graphical user interface.

# Other stuff

- `pdfmine.py your_file.pdf` to dump the text layer of a PDF to plaintext.
- `tokencounter.py` to estimate the amount of tokens that the text file has for a rough token usage estimate.
- `splitter.py textfile.txt` to split the text file into pieces that are more suitable for LLM's such as GPT-3.5 or GPT-4. It splits at 5000 chars at newline by default, but can be adjusted from the `char_limit` variable.
- `splitter.py` also tries to auto-sanitize tha pdf dump at the moment -- this might not be suitable for your use case scenario, so again -- look at the split dumps first before you run it through a LLM translation -- GIGO (garbage in, garbage out) applies to NLP translations as well.
- (Coming soon) pipeline to automate the actual translation process.

# Changelog
- v0.13 - added `pdfget.py` for natural reading order extraction using fitz (PyMuPDF)
- v0.12 - early alpha test for the GUI; `gui-translator.py`
- v0.11 - bugfixes
- v0.10 - translation combining via `combine_translation.py`
- v0.09 - token handling, naming policy
- v0.08 - more changes to the API call functionality
- v0.07 - API call updated and fixed for openai >v1.0
- v0.06 - fixes to the API call
- v0.05 - calculate the cost approximation
- v0.04 - calculate both tokens and chars
- v0.03 and earlier: rudimentary sketches

# Todo
- More streamlined automation for the translation process
- Perhaps an optional GUI with a PDF reader
- Looking into PDF file layers to see if we could replace the contents in-place (get text block layer from PDF page => sanitize => LLM translate => insert back in-place)

# About

- Started as a Grindmas (= Code-Grinding Christmas) project for [Skrolli magazine](https://skrolli.fi)
- [FlyingFathead](https://github.com/FlyingFathead) w/ code whispers from ChaosWhisperer
