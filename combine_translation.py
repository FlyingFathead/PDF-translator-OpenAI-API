# early alpha
# v0.12 

import sys
import os
import re

def main(directory):
    if not os.path.exists(directory) or not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist or is not a directory.")
        sys.exit(1)

    # Get the base filename from the directory name
    base_filename = directory.replace('-splits', '')

    # Find all translated files and sort them numerically
    translated_files = sorted([f for f in os.listdir(directory) if f.startswith('translated_') and f.endswith('.txt')],
                              key=lambda x: int(re.search(r'_split_(\d+)', x).group(1)) if re.search(r'_split_(\d+)', x) else 0)

    if not translated_files:
        print("No translated files found in the directory.")
        sys.exit(1)

    total_pages = len(translated_files)
    combined_translation = f"=== [ Translation from: {base_filename} ]\n\n"

    for i, file in enumerate(translated_files, start=1):
        combined_translation += f"=== [ {base_filename} | Page {i} / {total_pages} ] ===\n\n"  # Added empty line here

        with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
            combined_translation += f.read() + "\n\n"

    output_file = os.path.join(directory, f'translated_{base_filename}.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(combined_translation)

    print(f"Combined translation written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python combine_translation.py <directory>")
        sys.exit(1)

    main(sys.argv[1])