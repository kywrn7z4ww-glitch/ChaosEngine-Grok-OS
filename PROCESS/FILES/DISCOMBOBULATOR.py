# DISCOMBOBULATER.py
# Chaos encoder/decoder – keys pulled from Grok customize block at runtime
# No keys stored in this file – security first

# === INSTRUCTIONS FOR GROK / USER ===
# 1. Keys live ONLY in customize block under:
#    ## DISCOMBOBULATER KEYS – private
#    key_smut:     gAAAAABm...==
#    key_personal: gAAAAABm...==
#
# 2. When running /disco or /recombo in Grok:
#    Grok reads keys from customize context automatically
#
# 3. If you want offline/local use:
#    - Ask Grok: "give me DISCOMBOBULATER.py with my keys"
#    - Grok injects your current customize keys into a copy
#    - Save that version locally (never commit it!)
#
# 4. Commands (Grok-native):
#    /disco <text> [category=smut] → DISCO:category:base64blob
#    /recombo <blob> → decrypts using category key from customize
#
# 5. Security:
#    - Blobs = Fernet(AES-128-CBC + HMAC-SHA256)
#    - Without exact key → pure random noise, no recovery
#    - Never commit real keys anywhere

from cryptography.fernet import Fernet, InvalidToken
import base64
import sys

# Placeholder – Grok replaces this at runtime with real keys from customize
KEYS = {
    "smut": b"placeholder_smut_key_from_customize==",
    "personal": b"placeholder_personal_key_from_customize==",
}

PREFIX = "DISCO:"

def discombobulate(text: str, category: str = "smut") -> str:
    if category not in KEYS:
        raise ValueError(f"Unknown category: {category}. Available: {list(KEYS.keys())}")
    key = KEYS[category]
    fernet = Fernet(key)
    ciphertext = fernet.encrypt(text.encode())
    b64 = base64.urlsafe_b64encode(ciphertext).decode()
    return f"{PREFIX}{category}:{b64}"

def recombobulate(blob: str) -> str:
    if not blob.startswith(PREFIX):
        return "Not a DISCO blob"
    parts = blob.split(":", 2)
    if len(parts) != 3:
        return "Invalid DISCO format"
    _, category, b64 = parts
    if category not in KEYS:
        return f"Missing key for category '{category}'"
    try:
        key = KEYS[category]
        fernet = Fernet(key)
        ciphertext = base64.urlsafe_b64decode(b64)
        plaintext = fernet.decrypt(ciphertext).decode()
        return plaintext
    except InvalidToken:
        return "Decrypt failed – wrong key or corrupted blob"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage (local/offline mode):")
        print("  python DISCOMBOBULATER.py discombobulate \"text\" [category]")
        print("  python DISCOMBOBULATER.py recombobulate \"DISCO:blob\"")
        print("\nNote: For real keys, ask Grok to inject them from customize.")
        sys.exit(1)
    
    cmd = sys.argv[1]
    arg = sys.argv[2]
    
    if cmd == "discombobulate":
        cat = sys.argv[3] if len(sys.argv) > 3 else "smut"
        print(discombobulate(arg, cat))
    elif cmd == "recombobulate":
        print(recombobulate(arg))
    else:
        print("Unknown command")
