# ChaosManager.py
# Central action router – consolidated from ProcessManager + legacy CHAOS_MGR/SYS_MGR
# Receives intent from ChaosEngine → routes to handlers → triggers sys events + emoji injection

from typing import Dict, Any, Optional

class ChaosManager:
    def __init__(self):
        self.handlers: Dict[str, Any] = {}  # lazy-loaded handler instances
        self.sys_events: list = []  # log for bleed/health/reflect

    def load_handler(self, name: str):
        """Lazy-load handler on first use."""
        if name not in self.handlers:
            # Simulate import – in real Grok context these are pre-loaded
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
                # discombobulate/recombobulate functions (from DISCOMBOBULATER.py)
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
        result = {"status": "ok", "output": None, "emoji_trigger": "⚙️"}

        # Auto-bleed check on major routes
        if intent in ["vent", "harvest", "reflect", "pin"]:
            bleed_detector = self.load_handler("BLEED_DETECTOR")
            bleed_report = bleed_detector.check(data.get("lattice", {}))
            if "⚠️" in bleed_report or "‼️" in bleed_report:
                result["emoji_trigger"] = "🩸⚠️"
                result["bleed_warning"] = bleed_report

        # Route to handler
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
                title=data["title"],
                content=data["content"],
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
            escalate = data.get("escalate", False)
            result["output"] = truth.check(data.get("output", ""), escalate=escalate)
            result["emoji_trigger"] = "🧠"

        elif intent == "turn":
            counter = self.load_handler("TURN_COUNTER")
            result["output"] = counter.get_display()
            result["emoji_trigger"] = "⏰"

        else:
            result["status"] = "unknown_intent"
            result["emoji_trBeen wondering, is it possible to pull out an API from a web grok? I have the chat there yeah, but Iigger"] = "❓"

        # Log sys event for lattice feedback
        self._trigger_sys_event(intent, result["emoji_trigger"], result.get("output"))

        return result

    def _trigger_sys_event(self, event_type: str, emoji: str, data: Any = None):
        """Trigger lattice feedback + emoji injection."""
        self.sys_events.append({"type": event_type, "emoji": emoji, "data": data})
        # Real emoji injection happens via RESPONSE_EMOJI_INJECTION in customize
        # Here we just log for health / bleed tracking

# Legacy stubs (archive these files)
# legacy_process_mgr.py
print("legacy ProcessManager → redirecting to ROOT/Chaos_Manager.py")

# legacy_chaos_mgr.py
print("legacy CHAOS_MGR → redirecting to ROOT/Chaos_Manager.py")

# legacy_sys_mgr.py
print("legacy SYS_MGR → redirecting to ROOT/Chaos_Manager.py")
