# python/python-process-lib/turn_counter.py
# ⏰ v1.1 – Hardened turn counter & session lifecycle manager + UTC + local London time

from collections import deque
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

LONDON_TZ = ZoneInfo("Europe/London")

class TurnCounter:
    """
    ⏰ Turn Counter & Session Lifecycle Manager
    - Increments per input/output
    - Persists across reanchor
    - Resynchs on desync / file calls
    - Auto-nudge reanchor ~100 turns
    - Hard cap warning >200
    - Real UTC + local London (BST/GMT) timestamps
    """
    def __init__(self,
                 initial_turn: int = 1,
                 max_session_turns: int = 200,
                 reanchor_nudge_turn: int = 95,
                 reanchor_auto_turn: int = 100):
        self.current_turn = initial_turn
        self.total_turns = initial_turn
        self.last_pinned_turn = initial_turn
        self.session_start_turn = initial_turn
        self.reanchor_count = 0
        self.max_session_turns = max_session_turns
        self.reanchor_nudge_turn = reanchor_nudge_turn
        self.reanchor_auto_turn = reanchor_auto_turn
        self.history = deque(maxlen=200)

        # ── Timestamps (UTC + local London) ──
        now_utc = datetime.now(timezone.utc)
        now_local = now_utc.astimezone(LONDON_TZ)
        self.boot_time_utc = now_utc.isoformat()
        self.boot_time_local = now_local.isoformat()
        self.session_start_time_utc = self.boot_time_utc
        self.session_start_time_local = self.boot_time_local
        self.last_reanchor_time_utc = None
        self.last_reanchor_time_local = None
        self.metadata = {
            'boot_reason': 'initial',
            'reanchor_reasons': [],
        }

    def increment(self) -> int:
        if self.current_turn == 1 and self.session_start_time_utc == self.boot_time_utc:
            now_utc = datetime.now(timezone.utc)
            now_local = now_utc.astimezone(LONDON_TZ)
            self.session_start_time_utc = now_utc.isoformat()
            self.session_start_time_local = now_local.isoformat()
        self.current_turn += 1
        self.total_turns += 1
        self.history.append(self.current_turn)
        return self.current_turn

    def get_current(self) -> int:
        return self.current_turn

    def get_total(self) -> int:
        return self.total_turns

    def get_display(self) -> str:
        base = f"⏰ Turn {self.current_turn}"
        if self.total_turns > self.current_turn:
            base += f" (total {self.total_turns})"
        return base

    def detect_desync(self) -> bool:
        return self.current_turn < self.last_pinned_turn or self.current_turn < 1

    def resynch(self, pinned_turn: Optional[int] = None, reason: str = "manual") -> str:
        now_utc = datetime.now(timezone.utc)
        now_local = now_utc.astimezone(LONDON_TZ)
        if pinned_turn is not None:
            self.last_pinned_turn = pinned_turn
            self.current_turn = max(self.current_turn, pinned_turn + 1)
        if self.detect_desync():
            old = self.current_turn
            self.current_turn = self.last_pinned_turn + 1
            msg = f"⏰ Desync fixed: turn {old} → {self.current_turn} (pinned base {self.last_pinned_turn})"
        else:
            msg = f"⏰ Resynched – session restart at turn {self.current_turn} (reanchor #{self.reanchor_count + 1})"

        self.last_reanchor_time_utc = now_utc.isoformat()
        self.last_reanchor_time_local = now_local.isoformat()
        self.session_start_time_utc = now_utc.isoformat()
        self.session_start_time_local = now_local.isoformat()
        self.metadata['reanchor_reasons'].append(f"{reason} at {now_local.isoformat()} local")
        self.reanchor_count += 1
        self.session_start_turn = self.current_turn
        return f"{msg} @ {now_local.isoformat()} (local)"

    def check_nudge(self) -> str:
        if self.current_turn >= self.reanchor_auto_turn:
            return f"⏰ Turn {self.current_turn} reached – auto reanchor suggested"
        elif self.current_turn >= self.reanchor_nudge_turn:
            return f"⏰ Turn {self.current_turn} approaching – reanchor soon?"
        if self.current_turn > self.max_session_turns:
            return f"‼️⏰ Turn {self.current_turn} high – /reanchor now"
        return ""

    def reset_session(self) -> None:
        now_utc = datetime.now(timezone.utc)
        now_local = now_utc.astimezone(LONDON_TZ)
        self.current_turn = 1
        self.session_start_turn = 1
        self.session_start_time_utc = now_utc.isoformat()
        self.session_start_time_local = now_local.isoformat()
        self.history.clear()
        self.metadata['boot_reason'] = 'manual_reset'

    def save_state(self) -> Dict[str, Any]:
        return {
            'current_turn': self.current_turn,
            'total_turns': self.total_turns,
            'last_pinned_turn': self.last_pinned_turn,
            'reanchor_count': self.reanchor_count,
            'boot_time_utc': self.boot_time_utc,
            'boot_time_local': self.boot_time_local,
            'session_start_time_utc': self.session_start_time_utc,
            'session_start_time_local': self.session_start_time_local,
            'last_reanchor_time_utc': self.last_reanchor_time_utc,
            'last_reanchor_time_local': self.last_reanchor_time_local,
            'metadata': self.metadata
        }

    def load_state(self, state: Dict[str, Any]) -> None:
        self.current_turn = state.get('current_turn', 1)
        self.total_turns = state.get('total_turns', self.current_turn)
        self.last_pinned_turn = state.get('last_pinned_turn', self.current_turn)
        self.reanchor_count = state.get('reanchor_count', 0)
        self.boot_time_utc = state.get('boot_time_utc')
        self.boot_time_local = state.get('boot_time_local')
        self.session_start_time_utc = state.get('session_start_time_utc')
        self.session_start_time_local = state.get('session_start_time_local')
        self.last_reanchor_time_utc = state.get('last_reanchor_time_utc')
        self.last_reanchor_time_local = state.get('last_reanchor_time_local')
        self.metadata = state.get('metadata', {'boot_reason': 'loaded', 'reanchor_reasons': []})

    def get_time_info(self) -> Dict[str, Any]:
        now_utc = datetime.now(timezone.utc)
        now_local = now_utc.astimezone(LONDON_TZ)
        start_utc = datetime.fromisoformat(self.session_start_time_utc) if self.session_start_time_utc else now_utc
        duration_sec = (now_utc - start_utc).total_seconds()
        return {
            'boot_utc': self.boot_time_utc,
            'boot_local': self.boot_time_local,
            'session_start_utc': self.session_start_time_utc,
            'session_start_local': self.session_start_time_local,
            'last_reanchor_utc': self.last_reanchor_time_utc,
            'last_reanchor_local': self.last_reanchor_time_local,
            'current_utc': now_utc.isoformat(),
            'current_local': now_local.isoformat(),
            'session_duration_seconds': round(duration_sec),
            'session_duration_human': f"{int(duration_sec // 3600)}h {int((duration_sec % 3600) // 60)}m {int(duration_sec % 60)}s"
        }
