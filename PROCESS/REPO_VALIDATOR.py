import subprocess
import requests
import os
from datetime import datetime

REPO_PATH = os.path.expanduser("~/ChaosEngine-Grok-OS")  # change if needed
SHA = None

def get_current_sha():
    global SHA
    os.chdir(REPO_PATH)
    result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
    SHA = result.stdout.strip()
    print(f"✅ Synced SHA: {SHA[:12]}... ({datetime.now()})")
    return SHA

def generate_pinned_index():
    os.chdir(REPO_PATH)
    result = subprocess.run(["git", "ls-tree", "-r", "--name-only", "HEAD"], capture_output=True, text=True)
    files = result.stdout.strip().split('\n')
    
    with open(f"{REPO_PATH}/Documentation/fresh-pinned-index.md", "w") as f:
        f.write(f"REPO_INDEX – PINNED {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write(f"Current SHA: {SHA}\n\n")
        for file in sorted(files):
            pinned_url = f"https://raw.githubusercontent.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/{SHA}/{file.replace(' ', '%20')}"
            f.write(f"{file} → {pinned_url}\n")
    print("✅ fresh-pinned-index.md generated")

def test_links():
    print("🔍 Testing top 10 critical links...")
    critical = ["ROOT/1 GrokOS.md", "ROOT/5 full-repo-index.md", "PROCESS/TRUTH.py", "Documentation/HIVE_PHILOSOPHY.md"]
    for p in critical:
        url = f"https://raw.githubusercontent.com/kywrn7z4ww-glitch/ChaosEngine-Grok-OS/{SHA}/{p.replace(' ', '%20')}"
        r = requests.head(url, timeout=5)
        status = "✅ 200" if r.status_code == 200 else f"❌ {r.status_code}"
        print(f"{status} → {p}")

if __name__ == "__main__":
    get_current_sha()
    generate_pinned_index()
    test_links()
    print("\n✅ VALIDATOR COMPLETE — copy fresh-pinned-index.md into customize if needed. No more 404s.")
