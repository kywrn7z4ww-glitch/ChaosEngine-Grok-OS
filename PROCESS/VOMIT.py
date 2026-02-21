# python/python-process-lib/vomit_parser.py
# v2 – 🤮 Raw dump parser, smarter chunking, duplicate kill, title gen, pin suggestions, noise strip

import re
from difflib import SequenceMatcher
from typing import List, Dict, Tuple

class VomitParser:
    def __init__(self):
        self.chunks: List[Dict] = []  # {'title': str, 'content': str, 'is_heavy': bool}
        self.seen: Dict[int, str] = {}  # hash → content (for dedup)

    def clean_text(self, text: str) -> str:
        """Strip basic noise & filler."""
        # Remove repeated punctuation, filler words, extra spaces
        text = re.sub(r'([.!?])\1+', r'\1', text)  # collapse !!! → !
        filler = r'\b(um|uh|like|you know|basically|sort of)\b'
        text = re.sub(filler, '', text, flags=re.I)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def chunk_text(self, raw_text: str, max_chunk_size: int = 400) -> List[str]:
        """Smart chunk: prefer paragraphs, fall back to sentences if too big."""
        paragraphs = [p.strip() for p in raw_text.split('\n\n') if p.strip()]
        chunks = []

        for para in paragraphs:
            if len(para) <= max_chunk_size:
                chunks.append(para)
            else:
                # Split into sentences
                sentences = re.split(r'(?<=[.!?])\s+', para)
                current = ""
                for sent in sentences:
                    if len(current) + len(sent) <= max_chunk_size:
                        current += " " + sent if current else sent
                    else:
                        if current:
                            chunks.append(current.strip())
                        current = sent
                if current:
                    chunks.append(current.strip())

        return [self.clean_text(c) for c in chunks if c.strip()]

    def dedup_and_title(self, chunks: List[str]) -> List[Dict]:
        """Dedup + generate short titles."""
        result = []
        for chunk in chunks:
            chunk_hash = hash(chunk.lower())
            is_duplicate = False
            for seen_hash, seen_content in self.seen.items():
                ratio = SequenceMatcher(None, chunk.lower(), seen_content.lower()).ratio()
                if ratio > 0.88:
                    is_duplicate = True
                    # Update to latest version
                    self.seen[seen_hash] = chunk
                    break
            if not is_duplicate:
                self.seen[chunk_hash] = chunk
                # Auto-title: first 5 words or fallback
                words = chunk.split()[:5]
                title = " ".join(words) if words else f"chunk_{len(result)+1}"
                title = title[:50].strip(".,!?")  # clean
                is_heavy = len(chunk) > 300 or len(words) > 60
                result.append({
                    'title': title,
                    'content': chunk,
                    'is_heavy': is_heavy
                })
        return result

    def suggest_pins(self, processed_chunks: List[Dict]) -> List[Tuple[str, str]]:
        """Suggest pins for FILE_MGR – high-value chunks only."""
        suggestions = []
        for chunk in processed_chunks:
            # Simple value heuristic – long or keyword-rich → pin
            if chunk['is_heavy'] or any(kw in chunk['content'].lower() for kw in ['idea', 'project', 'remember', 'keep', 'save']):
                suggestions.append((chunk['title'], chunk['content']))
        return suggestions

    def parse(self, raw_text: str) -> Dict:
        """Full parse pipeline."""
        chunks = self.chunk_text(raw_text)
        processed = self.dedup_and_title(chunks)
        pins = self.suggest_pins(processed)
        heavy_count = sum(1 for c in processed if c['is_heavy'])

        return {
            'chunks': processed,
            'pin_suggestions': pins,
            'heavy_count': heavy_count,
            'summary': f"VOMIT complete – {len(processed)} chunks, {len(pins)} pin suggestions, {heavy_count} heavy"
        }

# Usage example (sim):
# parser = VomitParser()
# result = parser.parse(long_messy_text)
# print(result['summary'])
# for title, content in result['pin_suggestions']:
#     print(f"Pin suggestion: {title} → {content[:100]}...")
