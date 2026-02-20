# python/python-process-lib/vomit_parser.py
# v1 – 🤮 Raw dump parser, chunker, duplicate killer

from difflib import SequenceMatcher

class VomitParser:
    def __init__(self):
        self.chunks = []
        self.seen = {}  # content_hash → chunk

    def parse(self, raw_text: str, max_chunks: int = 6) -> list:
        """Chunk, dedup, clean raw dump."""
        # Simple split by double newline or long sentences
        raw_chunks = [c.strip() for c in raw_text.split('\n\n') if c.strip()]
        if len(raw_chunks) > max_chunks:
            raw_chunks = raw_chunks[:max_chunks]

        for chunk in raw_chunks:
            chunk_hash = hash(chunk.lower())
            duplicate = False
            for seen_hash, seen_chunk in self.seen.items():
                ratio = SequenceMatcher(None, chunk.lower(), seen_chunk.lower()).ratio()
                if ratio > 0.85:
                    duplicate = True
                    # Keep latest
                    self.seen[seen_hash] = chunk
                    break
            if not duplicate:
                self.seen[chunk_hash] = chunk
                self.chunks.append(chunk)

        return self.chunks

    def route_suggestions(self, chunks: list) -> list:
        """Suggest routes after parsing."""
        routes = []
        for chunk in chunks:
            if len(chunk) > 200:  # dense
                routes.append("VOMIT → FILE_MGR (pin clean chunk)")
            elif "contradict" in chunk.lower() or "fact" in chunk.lower():
                routes.append("TRUTH🧠")
            elif "health" in chunk.lower() or "bleed" in chunk.lower():
                routes.append("SYS_MGR⚙️")
            else:
                routes.append("CHAOS_MGR⚡ (review)")
        return routes

# Usage:
# parser = VomitParser()
# chunks = parser.parse(long_text)
# print(parser.route_suggestions(chunks))
