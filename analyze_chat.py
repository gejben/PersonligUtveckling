import re
import os

def parse_chat_log(file_path):
    print(f"Reading file: {file_path}")
    encodings = ['utf-8', 'utf-16', 'latin-1']
    content = None
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            print(f"Successfully read with encoding: {encoding}")
            break
        except Exception as e:
            print(f"Failed with encoding {encoding}: {e}")
            
    if content is None:
        print("Could not read file with any encoding.")
        return

    lines = content.split('\n')
    print(f"Total lines: {len(lines)}")
    
    # Regex for WhatsApp message format: "7/10/24, 10:39 - Gabriel: Message"
    msg_pattern = re.compile(r'^(\d{1,2}/\d{1,2}/\d{2}), (\d{1,2}:\d{2}) - ([^:]+): (.*)')
    
    # Expanded Keyword Categories
    keyword_map = {
        "Firsts": ["första gången", "first time", "första dejt", "first date", "första kyss", "first kiss"],
        "Locations": ["restaurang", "restaurant", "hotell", "hotel", "bio", "cinema", "café", "fika", "hemma hos", "din lägenhet", "mitt ställe", "stan", "park", "skogen", "sjö", "promenad", "walk"],
        "Travel": ["resa", "trip", "travel", "semester", "vacation", "åkte till", "went to", "bil", "tåg", "flyg"],
        "Media": ["titta på", "såg", "film", "movie", "serie", "series", "lyssna", "låt", "song", "musik", "music", "spela", "game", "bok", "läsa", "läser"],
        "Food_Drink": ["middag", "dinner", "lunch", "frukost", "breakfast", "äta", "åt", "dricka", "drack", "vin", "öl", "kaffe", "sushi", "pizza", "tacos"],
        "Activities": ["tränade", "gym", "springa", "löpning", "bad", "bada", "simma", "grilla", "fiska"],
        "Emotions": ["älskar dig", "love you", "kär", "love", "saknar dig", "miss you", "tycker om dig", "gillar dig"],
        "Intimacy": ["sov", "sover", "säng", "natt", "vakna", "kyss", "puss", "hålla hand", "kram"],
        "Gifts": ["present", "gav", "fick", "köpte", "julklapp", "födelsedag"]
    }
    
    results = []
    
    for line in lines:
        match = msg_pattern.match(line)
        if match:
            date, time, sender, message = match.groups()
            lower_msg = message.lower()
            
            found_categories = []
            found_keywords = []

            for category, kws in keyword_map.items():
                for kw in kws:
                    if kw in lower_msg:
                        found_categories.append(category)
                        found_keywords.append(kw)
                        # We don't break here to find multiple keywords/categories
            
            if found_categories:
                # Deduplicate
                found_categories = list(set(found_categories))
                found_keywords = list(set(found_keywords))
                
                results.append({
                    'date': date,
                    'time': time,
                    'sender': sender,
                    'message': message,
                    'categories': found_categories,
                    'keywords': found_keywords
                })

    out_file = r"c:\Users\ga-fie\personlig\expanded_analysis_results.md"
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# Expanded Chat Analysis Results\n\n")
        f.write(f"Total Matches: {len(results)}\n\n")
        
        current_date = ""
        for res in results:
            if res['date'] != current_date:
                f.write(f"## {res['date']}\n")
                current_date = res['date']
            
            # Format: **Time Sender**: Message `[Categories: Keywords]`
            cats_str = ", ".join(res['categories'])
            kws_str = ", ".join(res['keywords'])
            f.write(f"- **{res['time']} {res['sender']}**: {res['message']} `[{cats_str}: {kws_str}]`\n")

    print(f"Analysis complete. Results written to {out_file}")

file_path = r"c:\Users\ga-fie\personlig\WhatsApp Chat with Debbie.txt"
parse_chat_log(file_path)
