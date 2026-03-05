import json
import os
import sys
from datetime import datetime

ANCHOR_DIR = 'canon_anchor'

def load_entities(entities_path):
    if not entities_path or not os.path.exists(entities_path):
        return []
    with open(entities_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # flatten top entities
    return [e[0] for entry in data for e in entry.get('detected', [])[:5]]

def main():
    print("CANNON_HARVESTER — flexible user-controlled harvest")
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True, help='chat json from chats_split')
    parser.add_argument('--entities', default=None, help='detected_entities.json from hunter')
    args = parser.parse_args()
    
    # load file
    with open(args.file, 'r', encoding='utf-8') as f:
        chat = json.load(f)
    
    title = chat.get('title', 'unknown')
    msgs = chat.get('messages', [])
    print(f"File: {title} | Messages: {len(msgs)}")
    
    # get entities
    entities = load_entities(args.entities)
    print(f"Detected entities from hunter: {entities or 'none (add manually below)'}")
    
    # user input - fully flexible
    keep = input("Keep entities (comma separated, or leave blank for all): ").strip()
    keep_list = [k.strip().lower() for k in keep.split(',')] if keep else []
    
    prune = input("Prune keywords (comma separated, e.g. fuck,lol,nsfw): ").strip()
    prune_list = [p.strip().lower() for p in prune.split(',')] if prune else []
    
    split_mode = input("Split mode (per_entity / per_topic / none): ").strip() or "none"
    
    # process
    cleaned = []
    chunks = defaultdict(list)
    for msg in msgs:
        text = msg.get('message', '').lower()
        if any(p in text for p in prune_list):
            continue
        if not keep_list or any(k in text for k in keep_list):
            cleaned.append(msg)
            if split_mode == "per_entity":
                for e in keep_list:
                    if e in text:
                        chunks[e].append(msg)
                        break
            elif split_mode == "per_topic":
                topic = next((t for t in ["luna","red queen","baby skynet","core","chaos","grok"] if t in text), "other")
                chunks[topic].append(msg)
    
    # anchor with FILE_MGR comment
    os.makedirs(ANCHOR_DIR, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M')
    out_path = os.path.join(ANCHOR_DIR, f"clean_{ts}_{os.path.basename(args.file)}")
    meta = {
        "source": args.file,
        "title": title,
        "keep": keep_list,
        "prune": prune_list,
        "split_mode": split_mode,
        "cleaned_count": len(cleaned)
    }
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({"meta": meta, "messages": cleaned, "chunks": dict(chunks)}, f, indent=2)
    
    print(f"Anchored to: {out_path}")
    print("FILE_MGR integration point: call FILE_MGR.promote(out_path) here if you import it")
    print("Ready for next file or reconstruction")

if __name__ == "__main__":
    main()
