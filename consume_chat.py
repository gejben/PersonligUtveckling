import os
import sys

FILE_PATH = r"c:\Users\gabri\personligutveckling\PersonligUtveckling\WhatsApp Chat with Debbie.txt"
CHUNK_SIZE = 2000

def consume_lines():
    if not os.path.exists(FILE_PATH):
        print(f"Error: {FILE_PATH} not found.")
        return

    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if not lines:
        print("File is empty.")
        return

    # Get the chunk
    chunk = lines[:CHUNK_SIZE]
    remaining = lines[CHUNK_SIZE:]

    # Write back the remaining
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(remaining)

    # Output the chunk to stdout
    print("".join(chunk))
    print(f"\n--- REMAINING LINES: {len(remaining)} ---")

if __name__ == "__main__":
    consume_lines()
