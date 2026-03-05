import json
import os
import re
from datetime import datetime
from collections import defaultdict

# ====================== CONFIG ======================
ANCHOR_DIR = 'canon_anchor'          # where clean canon lives
INPUT_DIR = 'chats_split'            # your split files
TIER_S_KEYWORDS = ['chaosengine', 'grok os', 'lattice', 'emotionnet', 'baby skynet', 'core personality', 'zerg', 'queen']
FLUFF_KILL = ['lol', 'haha', 'lmao', 'xd', 'kk', 'ok', 'k', 'yeah', 'yep', 'nope', 'brb']

# ====================== ANCHOR STATE ======================
anchor_state = {
    "harvested_turns": 0,
    "canon_nodes": defaultdict(list),   # key = entity (lattice/core/baby_skynet)
    "last_anchor_time": datetime.now().isoformat()
}

def describe_chat(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        chat = json.load(f)
    
    title = chat.get('title', 'Untitled')
    chat_id = chat.get('id')
    msgs = chat.get('messages', [])
    
    keywords_found = [k for k in TIER_S_KEYWORDS if k.lower() in title.lower() or any(k.lower() in m['message'].lower() for m in msgs)]
    tier = 'S' if keywords_found else 'B'
    
    print(f"\n🩸 CANNON SCAN — {title} ({chat_id})")
    print(f"   Messages: {len(msgs)} | Tier: {tier} | Keywords: {keywords_found or 'none'}")
    print(f"   First msg: {msgs[0]['message'][:120]}..." if msgs else "empty")
    return chat, tier, keywords_found

def harvest_and_anchor(chat, keep_rules, prune_rules, split_mode="none"):
    # keep_rules = list of strings or entities to KEEP
    # prune_rules = list of keywords to delete
    # split_mode = "per_char" | "per_topic" | "per_turn" | "none"
    
    cleaned = []
    chunks = defaultdict(list)  # for splitter
    
    for msg in chat.get('messages', []):
        text = msg['message']
        lower = text.lower()
        
        # PRUNE
        if any(p.lower() in lower for p in prune_rules):
            continue
        if len(text.split()) <= 2 and any(f in lower for f in FLUFF_KILL):
            continue
        
        # KEEP filter
        if keep_rules and not any(k.lower() in lower for k in keep_rules):
            continue
        
        cleaned.append(msg)
        
        # SPLIT logic
        if split_mode == "per_topic":
            topic = next((t for t in ["lattice", "emotionnet", "baby_skynet", "core", "zerg"] if t in lower), "other")
            chunks[topic].append(msg)
        elif split_mode == "per_char":
            # simple sender-based
            chunks[msg.get('sender', 'unknown')].append(msg)
    
    # Update anchor state
    global anchor_state
    anchor_state["harvested_turns"] += len(cleaned)
    for node in keep_rules:
        anchor_state["canon_nodes"][node].extend([m['message'][:200] for m in cleaned if node.lower() in m['message'].lower()])
    
    # Save anchor log
    os.makedirs(ANCHOR_DIR, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M')
    anchor_path = os.path.join(ANCHOR_DIR, f"anchor_{ts}.json")
    with open(anchor_path, 'w', encoding='utf-8') as f:
        json.dump({"state": anchor_state, "cleaned_count": len(cleaned)}, f, indent=2)
    
    return cleaned, chunks, anchor_path

if __name__ == "__main__":
    print("🩸 CANNON_HARVESTER_v2 — CANON ANCHOR MODE")
    print("Usage: python CANNON_HARVESTER_v2.py <chat_filename.json> [keep=entity1,entity2] [prune=fluff,nsfw] [split=per_topic]")
    
    import sys
    if len(sys.argv) < 2:
        print("Drop a filename from chats_split/ as arg or paste full path")
        exit(1)
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        file_path = os.path.join(INPUT_DIR, file_path)
    
    chat, tier, keywords = describe_chat(file_path)
    
    # Example interactive — in real run you’ll edit or pipe args
    print("\nTell me next turn:")
    print("   keep=lattice,core,baby_skynet")
    print("   prune=smut,fluff,contradiction")
    print("   split=per_topic")
    print("or just say 'anchor all' for default sacred extraction")
