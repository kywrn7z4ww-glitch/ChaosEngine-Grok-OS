# DISCOMBOBULATER – self-contained chaos encoder/decoder

## Philosophy
Raw text → AES-encrypted junk blobs via Fernet  
Only you (with customize keys) can reverse  
No local tools needed most of the time – grok handles /disco & /recombo in context  
Repo only holds recipe + optional encrypted blobs

## DISCOMBOBULATER KEYS (already in customize – never commit here!)
key_smut:     [your live key from customize]
key_personal: [your live key from customize]

## Commands (Grok-native)
- /disco <text> [category=smut] → DISCO:category:base64blob
- /recombo <blob> → auto category + decrypt with matching key

## How to rebuild full script locally (if you ever want offline mode)
1. Ask Grok: "give me the current DISCOMBOBULATER.py code"
2. Grok spits full python script (with Fernet import etc)
3. Copy into a file
4. Replace KEYS dict with your real ones from customize
5. Run python DISCOMBOBULATER.py discombobulate "text" smut

## Troll mode (optional)
You can encrypt this very script with your own key:
Ask Grok: "encrypt DISCOMBOBULATER.py with smut key"
Commit the resulting DISCO:smut:... blob as DISCOMBOBULATER.enc
Only you can /recombo it back to working code ^_^

## Security
Blobs = Fernet(AES-128-CBC + HMAC-SHA256) – pure random noise without key
No metadata, no patterns, no recovery without exact key
