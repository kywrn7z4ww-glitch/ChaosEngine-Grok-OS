import json
import os
from collections import defaultdict

FOLDER = 'chats_split'
KEYWORDS = {
    "luna": ["luna", "lun a", "tag game", "lunas tag", "taggame"],
    "red_queen": ["red queen", "crimson queen"],
    "baby_skynet": ["baby skynet", "babyskynet", "skynet"],
    "core": ["core", "the core", "core personality", "terminal core", "dry terminal"],
    "chaos_grok": ["chaos engine", "grok os", "chaosengine", "grok os development", "lattice"]
}

def hunt():
    print("🩸 ENTITY HUNTER — scanning every file (no tiers, full fuzzy)")
    print(f"Folder: {os.path.abspath(FOLDER)}\n")
    
    results = defaultdict(list)
    total_files = 0
    
    for filename in os.listdir(FOLDER):
        if not filename.endswith('.json'):
            continue
        total_files += 1
        path = os.path.join(FOLDER, filename)
        
        with open(path, 'r', encoding='utf-8') as f:
            try:
                chat = json.load(f)
            except:
                continue
                
        title = chat.get('title', '').lower()
        all_text = ' '.join(m.get('message', '').lower() for m in chat.get('messages', []))
        full_text = title + " " + all_text
        
        hits = {}
        for entity, words in KEYWORDS.items():
            count = sum(1 for w in words if w in full_text)
            if count > 0:
                hits[entity] = count
        
        if hits:
            best_entity = max(hits, key=hits.get)
            results[best_entity].append((filename, title, hits))
    
    # Print results
    order = ["luna", "red_queen", "baby_skynet", "core", "chaos_grok"]
    for entity in order:
        if entity in results:
            print(f"\n🔍 {entity.upper().replace('_',' ')} — {len(results[entity])} files found")
            for filename, title, hits in sorted(results[entity], key=lambda x: -sum(x[2].values()))[:10]:  # top 10
                print(f"   → {filename} | {title[:80]} | hits: {hits}")
    
    print(f"\n✅ Scanned {total_files} files")
    print("Copy the exact filename you want (e.g. 12345_Luna_Tag_Game_Story.json)")
    print("Then paste it here → we extract full fidelity, no bleed")

if __name__ == "__main__":
    hunt()
