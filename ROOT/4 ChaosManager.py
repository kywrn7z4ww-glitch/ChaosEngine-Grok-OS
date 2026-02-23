# ChaosManager.py
# Central action router – consolidated from ProcessManager + legacy CHAOS_MGR/SYS_MGR
# Receives intent from ChaosEngine → routes to handlers → triggers sys events + emoji injection

from typing import Dict, Any, Optional

class ChaosManager:
    def __init__(self):
        self.handlers: Dict[str, Any] = {}          # lazy-loaded handler instances
        self.sys_events: list = []                  # log for bleed/health/reflect

    def load_handler(self, name: str) -> Any:
        """Lazy-load handler on first use."""
        if name not in self.handlers:
            # In real Grok context these modules are assumed pre-available
            if name == "BLEED_DETECTOR":
                from bleed_detector import BleedDetector
                self.handlers[name] = BleedDetector(opposites={'ache': 'relief', 'frustr': 'satisf'})
            elif name == "CANNON_HARVESTER":
                from CANNON_HARVESTER import cannon_harvest
                self.handlers[name] = cannon_harvest
            elif name == "CHUNK_SPLITTER":
                from chunk_split import ChunkSplitter
                self.handlers[name] = ChunkSplitter()
            elif name == "DISCOMBOBULATER":
                from DISCOMBOBULATER import discombobulate, recombobulate
                self.handlers[name] = {"disco": discombobulate, "recombo": recombobulate}
            elif name == "FILE_MGR":
                from FILE_MGR import FileManager
                self.handlers[name] = FileManager()
            elif name == "SYS_HEALTH":
                from sys_health import SystemHealth
                self.handlers[name] = SystemHealth()
            elif name == "TRUTH":
                from truth import TruthChecker
                self.handlers[name] = TruthChecker(hist=[], lat={})
            elif name == "TURN_COUNTER":
                from turn_counter import TurnCounter
                self.handlers[name] = TurnCounter()
            elif name == "VOMIT":
                from vomit_parser import VomitParser
                self.handlers[name] = VomitParser()
            else:
                raise ValueError(f"Unknown handler: {name}")
        return self.handlers[name]

    def route_intent(self, intent: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Main routing hub – called by ChaosEngine after intent translation."""
        result: Dict[str, Any] = {
            "status": "ok",
            "output": None,
            "emoji_trigger": "⚙️"
        }

        # Auto-bleed check on major lattice-touching routes
        if intent in ["vent", "harvest", "reflect", "pin"]:
            bleed_detector = self.load_handler("BLEED_DETECTOR")
            bleed_report = bleed_detector.check(data.get("lattice", {}))
            if "⚠️" in bleed_report or "‼️" in bleed_report:
                result["emoji_trigger"] = "🩸⚠️"
                result["bleed_warning"] = bleed_report

        # Route to appropriate handler
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
            result["output"] = disco["recombo"](data.get("blob", ""))
            result["emoji_trigger"] = "🔓💗"

        elif intent == "pin":
            fm = self.load_handler("FILE_MGR")
            result["output"] = fm.pin(
                title=data.get("title", ""),
                content=data.get("content", ""),
                thread_id=data.get("thread_id", "main"),
                value=data.get("value", 0.5),
                turn=data.get("turn", 0)
            )
            result["emoji_trigger"] = "📌"

        elif intent == "health":
            health = self.load_handler("SYS_HEALTH")
            result["output"] = health.get_raw()
            result["emoji_trigger"] = "💗"

        elif intent == "truth":
            truth = self.load_handler("TRUTH")
            result["output"] = truth.check(
                data.get("output", ""),
                escalate=data.get("escalate", False)
            )
            result["emoji_trigger"] = "🧠"

        elif intent == "turn":
            counter = self.load_handler("TURN_COUNTER")
            result["output"] = counter.get_display()
            result["emoji_trigger"] = "⏰"

        else:
            result["status"] = "unknown_intent"
            result["emoji_trigger"] = "❓"

        # Log the event (with possible override)
        self._trigger_sys_event(intent, result["emoji_trigger"], result.get("output"))

        return result

    def _trigger_sys_event(self, event_type: str, base_emoji: str, data: Any = None) -> None:
        """Trigger lattice feedback + apply final emoji overrides."""
        event = {"type": event_type, "emoji": base_emoji, "data": data}
        self.sys_events.append(event)

        # Apply event-type specific emoji overrides (these win)
        if event_type == "disco":
            event["emoji"] = "🔒📦🧊"
        elif event_type == "recombo":
            datastr = str(data or "").lower()
            if "success" in datastr:
                event["emoji"] = "🔓💗♻️"
            elif "fail" in datastr or "error" in datastr:
                event["emoji"] = "💥🛡️"
            else:
                event["emoji"] = "🔓❓"

        # Note: actual emoji injection into response text should happen
        # in your customize / RESPONSE_EMOJI_INJECTION layer using event["emoji"]

# ────────────────────────────────────────────────
# Legacy redirection stubs (safe to archive or keep)
if __name__ == "__main__":
    print("legacy ProcessManager → redirecting to ROOT/ChaosManager.py")
    print("legacy CHAOS_MGR      → redirecting to ROOT/ChaosManager.py")
    print("legacy SYS_MGR        → redirecting to ROOT/ChaosManager.py")
