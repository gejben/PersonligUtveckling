import re
import collections
from datetime import datetime
import os

FILE_PATH = r"c:\Users\gabri\personligutveckling\PersonligUtveckling\WhatsApp Chat with Debbie.txt"

def parse_line(line):
    # Pattern for "M/D/YY, HH:MM - Sender: Message"
    # Adjusting for the format seen in logs: "7/10/24, 10:39 - Gabriel: Hej!"
    match = re.match(r'^(\d+/\d+/\d+), (\d+:\d+) - ([^:]+): (.+)$', line)
    if match:
        return {
            'date': match.group(1),
            'time': match.group(2),
            'sender': match.group(3),
            'message': match.group(4)
        }
    return None

def analyze_chat():
    if not os.path.exists(FILE_PATH):
        print(f"File not found: {FILE_PATH}")
        return

    stats = {
        'total_messages': 0,
        'by_sender': collections.Counter(),
        'by_month': collections.Counter(),
        'keywords': {
            'love': 0,
            'conflict': 0,
            'future': 0,
            'fun': 0
        },
        'timeline': [] # List of (Date, Type)
    }
    
    # Define keywords
    love_words = ['älskar', 'kär', 'saknar', 'fin', 'snygg', 'mys', 'puss']
    conflict_words = ['ledsen', 'tyst', 'jobbig', 'stress', 'panik', 'falla', 'bråka', 'irritera']
    future_words = ['flytta', 'barn', 'sambo', 'framtid', 'resa', 'planera']
    fun_words = ['haha', 'lol', 'kul', 'roligt', 'skratt']

    current_date = None
    
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                data = parse_line(line)
                if data:
                    stats['total_messages'] += 1
                    stats['by_sender'][data['sender']] += 1
                    
                    # Date parsing
                    try:
                        dt = datetime.strptime(data['date'], '%m/%d/%y')
                        month_key = dt.strftime('%Y-%m')
                        stats['by_month'][month_key] += 1
                    except ValueError:
                        continue

                    msg_lower = data['message'].lower()
                    
                    # Keyword check
                    if any(w in msg_lower for w in love_words):
                        stats['keywords']['love'] += 1
                    if any(w in msg_lower for w in conflict_words):
                        stats['keywords']['conflict'] += 1
                    if any(w in msg_lower for w in future_words):
                        stats['keywords']['future'] += 1
                    if any(w in msg_lower for w in fun_words):
                        stats['keywords']['fun'] += 1
                        
    except Exception as e:
        print(f"Error processing file: {e}")
        return

    print("### Chat Analysis Summary")
    print(f"Total Messages: {stats['total_messages']}")
    print("\n### Sender Balance")
    for sender, count in stats['by_sender'].items():
        print(f"- {sender}: {count} ({count/stats['total_messages']*100:.1f}%)")
        
    print("\n### Emotional Zones")
    print(f"- Affection/Love: {stats['keywords']['love']} mentions")
    print(f"- Conflict/Stress: {stats['keywords']['conflict']} mentions")
    print(f"- Future Planning: {stats['keywords']['future']} mentions")
    print(f"- Fun/Laughter: {stats['keywords']['fun']} mentions")

    print("\n### Timeline (Volume by Month)")
    sorted_months = sorted(stats['by_month'].items())
    for month, count in sorted_months:
        print(f"- {month}: {count} msgs")

if __name__ == "__main__":
    analyze_chat()
