from difflib import SequenceMatcher

def pin(self,
        title: str,
        content: str,
        thread_id: str = 'main',
        value: float = 0.5,
        turn: int = 0) -> str:

    path = f"/thread/{thread_id}" if thread_id != 'main' else "/user"

    # Check for similar existing in this path
    for existing_title, data in list(self.fs[path].items()):
        title_ratio = SequenceMatcher(None, title.lower(), existing_title.lower()).ratio()
        content_ratio = SequenceMatcher(None, content.lower(), data['full_content'].lower()).ratio()

        if title_ratio > 0.92 or content_ratio > 0.85:
            # Update in place
            data['full_content'] = content
            data['content'] = content[:500] + ('...' if len(content) > 500 else '')
            data['turn'] = turn
            data['value'] = max(data['value'], value)  # keep highest value
            data['thread'] = thread_id
            return f"Updated '{existing_title}' (previous turn {data['turn']}, now {turn}) under {path}"

    # No duplicate → normal dedup + create
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
        'value': value
    }

    if thread_id == 'main':
        self.global_pins[title] = compacted

    self.recent_pins.append((title, path))
    return f"Pinned '{title}' under {path} (value: {value:.2f})"
