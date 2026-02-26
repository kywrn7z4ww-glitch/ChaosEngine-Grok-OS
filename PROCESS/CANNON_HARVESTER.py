# CANNON_HARVESTER.py
# Standalone chat harvest & sift tool – fidelity first

import re
import json
import sys

# === INSTRUCTIONS ===
# Run in Grok: paste this code + raw_chat = "your pasted chunk"  
# Run local: python CANNON_HARVESTER.py "your chat text" mixed  

# Optional: encrypt function stub – replace with DISCOMBOBULATER if loaded  
def optional_encrypt(content, category="personal"):
    # Stub – call DISCOMBOBULATER /disco in Grok or add logic  
    return content  # plaintext if no encrypt  

def cannon_harvest(raw_text, mode="mixed", encrypt=None):
    # Size check – warn if too big  
    if len(raw_text) > 15000:
        return {"error": "Chunk too large – split into smaller sections (<15k chars)"}
    
    # 1. Split into turns (regex on speaker lines)  
    turns = re.split(r'(Human:|Assistant:|User:|Grok:|Mark:|xAI:)', raw_text, flags=re.I)
    parsed = []
    timeline = []
    conflicts = []
    char_arcs = {}  # per-char dumps  
    current_char = "none"
    
    for i in range(1, len(turns), 2):
        speaker = turns[i].strip(':').strip()
        content = turns[i+1].strip()
        
        # 2. Sift type (fuzzy keywords, sanitized)  
        type_guess = "other"
        if re.search(r'(rp|character|scene|arc|story)', content, re.I):
            type_guess = "story"
        elif re.search(r'(tool|spec|filesystem|project|build)', content, re.I):
            type_guess = "project"
        elif re.search(r'(vent|personal|thoughts|notes)', content, re.I):
            type_guess = "personal"
        elif re.search(r'(smut|spicy|sexual|rp sex)', content, re.I):
            type_guess = "smut"
        
        # 3. Detect characters (add your 4 names)  
        chars = re.findall(r'(Char1|Char2|SexualChar1|SexualChar2)', content, re.I)  # replace with your names  
        if chars:
            current_char = chars[0].lower()
            if current_char not in char_arcs:
                char_arcs[current_char] = []
            char_arcs[current_char].append({"turn": i//2, "speaker": speaker, "type": type_guess, "content": content})
        
        # 4. Flag conflicts  
        if re.search(r'(contradiction|conflict|inconsistent|confuse)', content, re.I):
            conflicts.append({"turn": i//2, "content": content})
        
        parsed.append({
            "turn": i//2,
            "speaker": speaker,
            "type": type_guess,
            "char": current_char,
            "content": content
        })
        
        timeline.append({
            "turn": i//2,
            "event": f"{speaker}: {type_guess} - {content[:50]}..."  # timeline summary  
        })
    
    # 5. Optional encrypt on outputs  
    outputs = {
        "full_parsed": json.dumps(parsed, indent=2),
        "timeline": json.dumps(timeline, indent=2),
        "conflicts": json.dumps(conflicts, indent=2),
        "char_arcs": json.dumps(char_arcs, indent=2)
    }
    
    if encrypt:
        for k in outputs:
            outputs[k] = optional_encrypt(outputs[k], encrypt)
    
    return outputs

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python CANNON_HARVESTER.py \"chat text\" [mode] [encrypt]")
        sys.exit(1)
    
    raw_text = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "mixed"
    encrypt = sys.argv[3] if len(sys.argv) > 3 else None
    
    result = cannon_harvest(raw_text, mode, encrypt)
    print(json.dumps(result, indent=2))
