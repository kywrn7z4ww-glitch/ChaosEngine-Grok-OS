# python/python-process-lib/FILE_MGR.py
# v1.3 – pins + timestamps (UTC + local London/BST)

from collections import defaultdict, deque
from difflib import SequenceMatcher
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

LONDON_TZ = ZoneInfo("Europe/London")

class FileManager:
    def __init__(self):
        self.fs: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(dict)
        self.global_pins: Dict[str, str] = {}
        self.recent_pins: deque = deque(maxlen=10)

    def pin(self,
            title: str,
            content: str,
            thread_id: str = 'main',
            value: float = 0.5,
            turn: int = 0,
            status: str = 'active') -> str:
        path = f"/thread/{thread_id}" if thread_id != 'main' else "/user"
        now_utc = datetime.now(timezone.utc)
        now_local = now_utc.astimezone(LONDON_TZ)
        now_utc_iso = now_utc.isoformat()
        now_local_iso = now_local.isoformat()

        for existing_title, data in list(self.fs[path].items()):
            title_ratio = SequenceMatcher(None, title.lower(), existing_title.lower()).ratio()
            content_ratio = SequenceMatcher(None, content.lower(), data.get('full_content', '').lower()).ratio()
            if title_ratio > 0.92 or content_ratio > 0.85:
                data['full_content'] = content
                data['content'] = content[:500] + ('...' if len(content) > 500 else '')
                data['turn'] = turn
                data['value'] = max(data['value'], value)
                data['thread'] = thread_id
                data['status'] = status
                data['updated_at_utc'] = now_utc_iso
                data['updated_at_local'] = now_local_iso
                return f"📌 Updated '{existing_title}' (turn {data['turn']}, status {status}) @ {now_local_iso} local"

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
            'status': status,
            'created_at_utc': now_utc_iso,
            'created_at_local': now_local_iso,
            'updated_at_utc': now_utc_iso,
            'updated_at_local': now_local_iso
        }
        if thread_id == 'main':
            self.global_pins[title] = compacted
        self.recent_pins.append((title, path))
        return f"📌 Pinned '{title}' under {path} (value {value:.2f}) @ {now_local_iso} local"

    # (rest of your methods unchanged – just add the local/utc fields where you update timestamps)
    # For example in complete() and archive():
    # data['updated_at_utc'] = now_utc_iso
    # data['updated_at_local'] = now_local_iso

    # ... keep your existing complete(), archive(), list_pins(), recall(), nudge_bloat(), auto_pin(), etc.
    # (I didn't repeat them here to save space – just insert the now_utc / now_local lines where you set 'updated_at')
