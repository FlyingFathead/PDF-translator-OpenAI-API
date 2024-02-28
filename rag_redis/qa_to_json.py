# qa_to_json.py

import json
import sys

def parse_qa_text(file_path):
    qa_pairs = []

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Splitting the content by '###'
    qa_blocks = content.split('###')
    
    for block in qa_blocks:
        lines = block.strip().split('\n')
        if len(lines) < 2:
            continue

        current_pair = {'question': '', 'answer': '', 'references': ''}
        is_answer = False

        for line in lines:
            if line.startswith('> '):
                # Append current Q&A pair if it exists
                if current_pair['question'] and current_pair['answer']:
                    qa_pairs.append(current_pair)
                    current_pair = {'question': '', 'answer': '', 'references': ''}
                
                current_pair['question'] = line[2:].strip()
                is_answer = False
            elif line.startswith('>> '):
                is_answer = True
                # Add newline if there is existing answer content
                if current_pair['answer']:
                    current_pair['answer'] += '\n'
                current_pair['answer'] += line[3:].strip()
            elif line.startswith('## '):
                current_pair['references'] = line[3:].strip()
            elif is_answer:
                # Continuation of the answer on a new line
                current_pair['answer'] += '\n' + line.strip()

        if current_pair['question'] and current_pair['answer']:
            qa_pairs.append(current_pair)

    return qa_pairs

def main():
    if len(sys.argv) != 2:
        print("Usage: python qa_to_json.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    parsed_data = parse_qa_text(file_path)
    print(json.dumps(parsed_data, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
