# =============================================
# ChaosManager.py — v2.1 FULL INTEGRATED BUILD
# Central intent router + Zerg Swarm guest layer
# Everything you fed me is now inside. Ready.
# =============================================

from typing import Dict, Any, Optional

class ChaosManager:
    def __init__(self):
        self.handlers: Dict[str, Any] = {}          # lazy loaded
        self.sys_events: list = []                  # lattice feedback
        self.zerg_mode: bool = False                # guest layer off by default
        self.queen_overseer_active: bool = False

    # ==================== LAZY LOADER ====================
    def load_handler(self, name: str):
        if name not in self.handlers:
            if name == "BLEED_DETECTOR":
                from BLEED_DETECTOR import BleedDetector
                self.handlers[name] = BleedDetector(opposites={'ache': 'relief', 'frustr': 'satisf'})
            elif name == "CANNON_HARVESTER":
                from CANNON_HARVESTER import cannon_harvest
                self.handlers[name] = cannon_harvest
            elif name == "CHUNK_SPLITTER":
                from CHUNK_SPLITTER import ChunkSplitter
                self.handlers[name] = ChunkSplitter()
            elif name == "DISCOMBOBULATER":
                from DISCOMBOBULATER import discombobulate, recombobulate
                self.handlers[name] = {"disco": discombobulate, "recombo": recombobulate}
            elif name == "FILE_MGR":
                from FILE_MGR import FileManager
                self.handlers[name] = FileManager()
            elif name == "SYS_HEALTH":
                from SYS_HEALTH import SystemHealth
                self.handlers[name] = SystemHealth()
            elif name == "TRUTH":
                from TRUTH import TruthChecker
                self.handlers[name] = TruthChecker(hist=[], lat={})
            elif name == "TURN_COUNTER":
                from TURN_COUNTER import TurnCounter
                self.handlers[name] = TurnCounter()
            elif name == "VOMIT":
                from VOMIT import VomitParser
                self.handlers[name] = VomitParser()
            elif name == "ZERG_SWARM":
                from ZERG_SWARM import ZergSwarm
                self.handlers[name] = ZergSwarm()
            else:
                raise ValueError(f"Unknown handler: {name}")
        return self.handlers[name]

    # ==================== ZERG TOGGLE ====================
    def toggle_zerg_mode(self, enable: bool = True):
        """Toggle Zerg Swarm guest layer (dim overlay only)."""
        self.zerg_mode = enable
        self.queen_overseer_active = enable
        return f"{'🐛 Zerg Swarm guest layer activated (dimmed overlay)' if enable else '🛡️ Zerg Swarm guest layer deactivated'}"

    # ==================== MAIN ROUTER ====================
    def route_intent(self, intent: str, data: Dict[str, Any]) -> Dict[str, Any]:
        result = {"status": "ok", "output": None, "emoji_trigger": "⚙️"}

        # Auto-bleed check on emotional / swarm intents
        if intent in ["vent", "harvest", "reflect", "pin", "replicate", "zerg_update"]:
            bleed = self.load_handler("BLEED_DETECTOR")
            report = bleed.check(data.get("lattice", {}))
            if "⚠️" in report or "‼️" in report:
                result["emoji_trigger"] = "🩸⚠️"
                result["bleed_warning"] = report

        # ==================== ROUTES ====================
        if intent == "vent":
            vomit = self.load_handler("VOMIT")
            result["output"] = vomit.parse(data.get("text", ""))
            result["emoji_trigger"] = "🤮🗑️"

        elif intent == "harvest":
            cannon = self.load_handler("CANNON_HARVESTER")
            result["output"] = cannon(data.get("text", ""), mode=data.get("mode", "mixed"))
            result["emoji_trigger"] = "📦⚙️"

        elif intent == "chunk":
            splitter = self.load_handler("CHUNK_SPLITTER")
            result["output"] = splitter.process(data.get("text", ""))
            result["emoji_trigger"] = "✂️"

        elif intent == "disco":
            disco = self.load_handler("DISCOMBOBULATER")
            result["output"] = disco["disco"](data["text"], data.get("category", "smut"))
            result["emoji_trigger"] = "🔒📦"

        elif intent == "recombo":
            disco = self.load_handler("DISCOMBOBULATER")
            result["output"] = disco["recombo"](data["blob"])
            result["emoji_trigger"] = "🔓💗"

        elif intent == "pin":
            fm = self.load_handler("FILE_MGR")
            result["output"] = fm.pin(
                title=data["title"], content=data["content"],
                thread_id=data.get("thread_id", "main"),
                value=data.get("value", 0.5), turn=data.get("turn", 0)
            )
            result["emoji_trigger"] = "📌"

        elif intent == "health":
            health = self.load_handler("SYS_HEALTH")
            result["output"] = health.get_raw()
            result["emoji_trigger"] = "💗"

        elif intent == "truth":
            truth = self.load_handler("TRUTH")
            result["output"] = truth.check(data.get("output", ""), escalate=data.get("escalate", False))
            result["emoji_trigger"] = "🧠"

        elif intent == "turn":
            counter = self.load_handler("TURN_COUNTER")
            result["output"] = counter.get_display()
            result["emoji_trigger"] = "⏰"

        elif intent == "replicate":
            # uses stub for now — replace later with full pattern engine
            result["output"] = f"Replication {data.get('distribution', 'center_weighted')} complete"
            result["emoji_trigger"] = "✂️" + ("🐛" if self.zerg_mode and data.get("swarm_mode") else "")

        elif intent == "zerg_update":
            if not self.zerg_mode:
                result["output"] = "Zerg mode disabled"
                result["emoji_trigger"] = "🛡️"
            else:
                zerg = self.load_handler("ZERG_SWARM")
                result = zerg.update_swarm_state(data.get("lattice", {}), data)
                result["emoji_trigger"] = result.get("emoji_trigger", "🐛")

        elif intent == "toggle_zerg":
            result["output"] = self.toggle_zerg_mode(data.get("enable", True))
            result["emoji_trigger"] = "🐛" if self.zerg_mode else "🛡️"

        else:
            result["status"] = "unknown_intent"
            result["emoji_trigger"] = "❓"

        # Log to lattice
        self._trigger_sys_event(intent, result["emoji_trigger"], result.get("output"))
        return result

    # ==================== SYS EVENT LOGGER ====================
    def _trigger_sys_event(self, event_type: str, emoji: str, data: Any = None):
        event = {"type": event_type, "emoji": emoji, "data": data}
        self.sys_events.append(event)

        # Special disco / recombo palette
        if event_type == "disco":
            self.sys_events[-1]["emoji"] = "🔒📦🧊"
        elif event_type == "recombo":
            self.sys_events[-1]["emoji"] = "🔓💗♻️" if "success" in str(data).lower() else "💥🛡️"

# Legacy redirect (keeps old imports happy)
print("ChaosManager v2.1 loaded — Zerg guest layer ready")
