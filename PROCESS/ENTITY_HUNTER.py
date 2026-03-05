import json
import os
import re
from collections import defaultdict

FOLDER = 'chats_split'
REPORT_FILE = 'detected_entities.json'

def detect_entities(text):
    # dynamic: capitalized phrases + repeated proper nouns
    candidates = re.findall(r'\b[A-Z][a-zA-Z0-9\s\'-]{2,}\b', text)
    freq = defaultdict(int)
    for c in candidates:
        clean = c.strip().lower()
        if len(clean) > 3 and not clean.isdigit():
            freq[clean] += 1
    # score = freq * spread
    return sorted([(ent, count) for ent, count in freq.items() if count >= 2], key=lambda x: -x[1])

def hunt():
    print("ENTITY_HUNTER — dynamic scan (no fixed keywords)")
    results = []
    for filename in os.listdir(FOLDER):
        if not filename.endswith('.json'):
            continue
        path = os.path.join(FOLDER, filename)
        with open(path, 'r', encoding='utf-8') as f:
            chat = json.load(f)
        title = chat.get('title', '')
        full_text = title + " " + " ".join(m.get('message', '') for m in chat.get('messages', []))
        entities = detect_entities(full_text)
        if entities:
            results.append({
                "file": filename,
                "title": title[:100],
                "detected": entities[:15]  # top 15
            })
    
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"Scanned {len(results)} files with entities")
    print(f"Report saved: {REPORT_FILE}")
    print("Next: python CANNON_HARVESTER.py --file <filename> --entities detected_entities.json")

if __name__ == "__main__":
    hunt()
