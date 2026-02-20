# python/python-process-lib/chunk_split.py
# ✂ v1.4 – Load-aware chunking & prediction (emoji in ALL output)

import re
from typing import List, Dict, Tuple

class ChunkSplitter:
    def __init__(self,
                 max_chunk_words: int = 400,
                 heavy_threshold_words: int = 800,
                 heavy_threshold_sentences: int = 60):
        self.max_chunk_words = max_chunk_words
        self.heavy_threshold_words = heavy_threshold_words
        self.heavy_threshold_sentences = heavy_threshold_sentences

    def predict_load(self, text: str) -> Tuple[str, int]:
        """✂ Estimate load: 'light' or 'heavy' + expected chunk count."""
        words = len(text.split())
        sentences = len(re.findall(r'[.!?]', text)) + 1
        complexity = sentences / (words / 100) if words > 0 else 0

        is_heavy = (words > self.heavy_threshold_words) or (complexity > 0.8)
        expected_chunks = max(1, (words // self.max_chunk_words) + 1)

        return "heavy" if is_heavy else "light", expected_chunks

    def clean_chunk(self, chunk: str) -> str:
        """Basic noise removal."""
        chunk = re.sub(r'([.!?])\1+', r'\1', chunk)          # collapse repeated punctuation
        chunk = re.sub(r'\b(um|uh|like|you know|basically)\b', '', chunk, flags=re.I)
        chunk = re.sub(r'\s+', ' ', chunk).strip()
        return chunk

    def split(self, text: str) -> List[str]:
        """✂ Smart split: prefer paragraphs, fall back to sentences."""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        chunks = []

        for para in paragraphs:
            para = self.clean_chunk(para)
            if len(para.split()) <= self.max_chunk_words:
                chunks.append(para)
            else:
                sentences = re.split(r'(?<=[.!?])\s+', para)
                current = ""
                for sent in sentences:
                    sent = sent.strip()
                    if not sent:
                        continue
                    if len(current.split()) + len(sent.split()) <= self.max_chunk_words:
                        current += " " + sent if current else sent
                    else:
                        if current:
                            chunks.append(current.strip())
                        current = sent
                if current:
                    chunks.append(current.strip())

        return [c for c in chunks if c]

    def process(self, raw_text: str) -> Dict:
        """✂ Full pipeline: predict → split → clean → summarize."""
        load_type, expected_chunks = self.predict_load(raw_text)
        chunks = self.split(raw_text)

        return {
            'raw_length_words': len(raw_text.split()),
            'load_type': load_type,
            'expected_chunks': expected_chunks,
            'actual_chunks': len(chunks),
            'chunks': chunks,
            'summary': f"✂ Load {load_type.upper()} – split into {len(chunks)} chunks (predicted {expected_chunks})"
        }

# Example usage:
# splitter = ChunkSplitter()
# result = splitter.process(long_text)
# print(result['summary'])
# for i, chunk in enumerate(result['chunks'], 1):
#     print(f"✂ Chunk {i} ({len(chunk.split())} words): {chunk[:120]}...")
