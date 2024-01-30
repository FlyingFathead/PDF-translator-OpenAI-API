import json
import sys

def parse_qa_text(file_path):
    qa_pairs = []

    with open(file_path, 'r') as file:
        content = file.read()

    # Splitting the content by '###'
    qa_blocks = content.split('###')
    
    for block in qa_blocks:
        lines = block.strip().split('\n')
        if len(lines) < 2:
            continue

        current_pair = {}
        for line in lines:
            if line.startswith('> '):
                current_pair['question'] = line[2:].strip()
            elif line.startswith('>> '):
                current_pair['answer'] = line[3:].strip()
            elif line.startswith('## '):
                current_pair['references'] = line[3:].strip()

        if 'question' in current_pair and 'answer' in current_pair:
            qa_pairs.append(current_pair)

    return qa_pairs

def main():
    if len(sys.argv) != 2:
        print("Usage: python qa_to_json.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    parsed_data = parse_qa_text(file_path)
    json_output = json.dumps(parsed_data, indent=4)
    print(json_output)

if __name__ == "__main__":
    main()
