# python/python-process-lib/FILE_MGR.py
# v1.2 – pins + duplicate update + complete/archive + 📌 emoji anchors
from collections import defaultdict, deque
from difflib import SequenceMatcher
from typing import Dict, Any, Optional

class FileManager:
    def __init__(self):
        # path -> title -> data dict
        self.fs: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(dict)
        # global fallback pins
        self.global_pins: Dict[str, str] = {}
        # recent for quick preview
        self.recent_pins: deque = deque(maxlen=10)

    def pin(self,
            title: str,
            content: str,
            thread_id: str = 'main',
            value: float = 0.5,
            turn: int = 0,
            status: str = 'active') -> str:
        """Add or update a pin. Overwrite on high similarity (duplicate handling)."""
        path = f"/thread/{thread_id}" if thread_id != 'main' else "/user"

        # Check for similar existing in this path
        for existing_title, data in list(self.fs[path].items()):
            title_ratio = SequenceMatcher(None, title.lower(), existing_title.lower()).ratio()
            content_ratio = SequenceMatcher(None, content.lower(), data.get('full_content', '').lower()).ratio()

            if title_ratio > 0.92 or content_ratio > 0.85:
                # Update in place (overwrite with latest version)
                data['full_content'] = content
                data['content'] = content[:500] + ('...' if len(content) > 500 else '')
                data['turn'] = turn
                data['value'] = max(data['value'], value)
                data['thread'] = thread_id
                data['status'] = status
                return f"📌 Updated '{existing_title}' (previous turn {data['turn']}, now {turn}, status {status}) under {path}"

        # No duplicate → normal dedup + create new
        original_title = title
        counter = 1
        while title in self.fs[path]:
            title = f"{original_title}_{counter}"
            counter += 1

        compacted = content[:500] + ('...' if len(content) > 500 else '')
        self.fs[path][title] = {
            'content': compacted,
            'full_content': content,
            'turn': turn,
            'thread': thread_id,
            'value': value,
            'status': status
        }

        if thread_id == 'main':
            self.global_pins[title] = compacted

        self.recent_pins.append((title, path))
        return f"📌 Pinned '{title}' under {path} (value {value:.2f}, status {status})"

    def complete(self, title: str, thread_id: Optional[str] = None) -> str:
        """Mark an item as complete (pre-archive step)."""
        for path in self.fs:
            if title in self.fs[path]:
                data = self.fs[path][title]
                if thread_id and data['thread'] != thread_id:
                    continue
                old_status = data['status']
                data['status'] = 'complete'
                return f"📌 Marked '{title}' complete (was {old_status}) in {path}. Use /archive '{title}' to move?"
        return f"No match for '{title}' to complete."

    def archive(self, title: str, thread_id: Optional[str] = None) -> str:
        """Move completed item to archive path."""
        for path in list(self.fs.keys()):
            if title in self.fs[path]:
                data = self.fs[path].pop(title)
                archive_path = '/archive/completed'
                self.fs[archive_path][title] = data
                return f"📌 Archived '{title}' from {path} to {archive_path} (status complete)"
        return f"No match for '{title}' to archive."

    def list_pins(self, thread_id: Optional[str] = None) -> str:
        """List pins with 📌 bullets and status."""
        lines = []
        if thread_id:
            path = f"/thread/{thread_id}"
            pins = self.fs.get(path, {})
            if pins:
                lines.append(f"{thread_id}: {len(pins)} pins")
                for title in list(pins)[:8]:  # limit preview
                    d = pins[title]
                    lines.append(f"  📌 {title} (turn {d['turn']}, status {d.get('status', 'active')})")
            else:
                lines.append(f"{thread_id}: no pins")
        else:
            # overview
            for path in ['/user', '/root', '/archive/completed']:
                pins = self.fs.get(path, {})
                if pins:
                    lines.append(f"{path}: {len(pins)} items")
        if self.recent_pins:
            recent_str = ", ".join([t for t, p in list(self.recent_pins)[-3:]])
            lines.append(f"Recent: {recent_str}")
        return "\n".join(lines) if lines else "No pins stored yet."

    def recall(self, title: str, thread_id: Optional[str] = None) -> str:
        """Recall full content with 📌 header."""
        candidates = []
        for path in self.fs:
            if title in self.fs[path]:
                data = self.fs[path][title]
                if thread_id and data['thread'] != thread_id:
                    continue
                candidates.append((title, path, data))
            # fuzzy startswith
            for t in self.fs[path]:
                if title.lower() in t.lower():
                    data = self.fs[path][t]
                    if thread_id and data['thread'] != thread_id:
                        continue
                    candidates.append((t, path, data))

        if not candidates:
            return f"No match for '{title}'."
        if len(candidates) > 1:
            matches = ", ".join([f"{t} ({p})" for t, p, _ in candidates])
            return f"Multiple matches: {matches} — specify more?"

        title, path, data = candidates[0]
        return f"📌 [{title}] from {path} (turn {data['turn']}, value {data['value']:.2f}, status {data.get('status', 'active')}):\n{data['full_content']}"

    def nudge_bloat(self, total_pins: int, total_vol: int) -> str:
        """Low-noise bloat warning with 🗑️ alias."""
        total = total_pins + total_vol
        if total > 25:
            return f"📦 Storage heavy ({total} items) — /🗑️ low-value? /📦 list"
        if total > 15:
            return f"📦 Storage at {total} items — consider /🗑️ or /archive low"
        return ""

    def auto_pin(self, txt: str, lattice_value: float, turn: int, thread_id: str = 'main') -> str:
        """Auto-detect and pin on keywords/high value."""
        lower = txt.lower()
        if any(kw in lower for kw in ['remember:', 'idea:', 'save this:', 'keep this', 'pin this']):
            title = txt.split(':', 1)[1].strip()[:40] if ':' in txt else f"auto_{turn}"
            return self.pin(title, txt, thread_id, lattice_value, turn)
        if lattice_value > 0.45:
            title = f"high_{turn}"
            return self.pin(title, txt, thread_id, lattice_value, turn)
        return 
        
            def auto_pin_from_intent(self, txt: str, lattice_value: float, turn: int, thread_id: str = 'main') -> str:
        """Auto-pin on keywords or high lattice value – call after every input."""
        lower = txt.lower()
        keywords = ['remember:', 'idea:', 'save this:', 'keep this', 'pin this', 'project:', 'task:']
        if any(kw in lower for kw in keywords) or lattice_value > 0.5:
            title = txt.split(':', 1)[1].strip()[:40] if ':' in txt else f"auto_{turn}"
            return self.pin(title, txt, thread_id, lattice_value, turn, status='active')
        return ""

    def auto_complete_detect(self, txt: str) -> str:
        """Detect 'finished' / 'done' language – suggest /complete."""
        lower = txt.lower()
        done_keywords = ['finished', 'done', 'complete this', 'project complete', 'task done']
        if any(kw in lower for kw in done_keywords):
            # Simple title guess – improve later with context
            title = "unknown_project"
            return f"Detected completion – /complete '{title}'? Y/N"
        return ""

    def archive_completed(self, title: str, thread_id: Optional[str] = None) -> str:
        """Move completed item to archive path."""
        for path in list(self.fs.keys()):
            if title in self.fs[path]:
                data = self.fs[path].pop(title)
                archive_path = '/archive/completed'
                self.fs[archive_path][title] = data
                return f"📦 Archived '{title}' from {path} to {archive_path} (status complete)"
        return f"No match for '{title}' to archive."""
