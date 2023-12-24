import re
import sys

def insert_empty_lines(text):
    # Step 1: Insert an empty line between each paragraph
    return re.sub(r'(\r?\n)(?!\r?\n)', r'\1\1', text)

def remove_extra_lines(text):
    # Step 2: Reduce multiple blank lines to a single blank line
    return re.sub(r'(\r?\n){2,}', r'\1\1', text)

def main():
    if len(sys.argv) != 2:
        print("Usage: post_process.py <file>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()

        # Perform the two-step process
        content = insert_empty_lines(content)
        content = remove_extra_lines(content)

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Processed file saved: {filename}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()