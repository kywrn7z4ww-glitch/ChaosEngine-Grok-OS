# ChaosManager.py
# Central action router – v2.0 overhaul
# Routes all intents, protects emotional core, treats Zerg Swarm as optional guest layer

from typing import Dict, Any, Optional
import random

class ChaosManager:
    def __init__(self):
        self.handlers: Dict[str, Any] = {}
        self.sys_events: list = []
        self.zerg_mode: bool = False  # off by default – guest layer only
        self.queen_overseer_active: bool = False  # read-only mirror

    def load_handler(self, name: str):
        """Lazy-load handler on first use."""
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
            elif name == "REPLICATE_PATTERN":
                self.handlers[name] = self._replicate_pattern_stub
            else:
                raise ValueError(f"Unknown handler: {name}")
        return self.handlers[name]

    def toggle_zerg_mode(self, enable: bool = True):
        """Toggle Zerg Swarm guest layer (off by default)."""
        self.zerg_mode = enable
        if enable:
            self.queen_overseer_active = True  # read-only mirror
            return "🐛 Zerg Swarm guest layer activated (dimmed overlay only)"
        else:
            self.queen_overseer_active = False
            return "🛡️ Zerg Swarm guest layer deactivated"

    def _replicate_pattern_stub(self, template_data: Dict, region: Dict, distribution: str = "center_weighted", swarm_mode: bool = False) -> Dict[str, Any]:
        """Procedural pattern replication – based on your Gensokyo replication script."""
        result = {"status": "ok", "output": None, "emoji_trigger": "✂️📦"}

        if not template_data or "items" not in template_data:
            result["status"] = "invalid_template"
            return result

        if distribution == "grid":
            result["output"] = f"Grid replication: {len(template_data['items'])} items placed in region"
        elif distribution == "random":
            result["output"] = f"Random replication: {len(template_data['items'])} items scattered"
        else:  # center_weighted default
            result["output"] = f"Center-weighted replication: {len(template_data['items'])} items clustered"

        # Optional Zerg swarm sync (dim overlay only)
        if swarm_mode and self.zerg_mode:
            result["swarm_sync"] = round(random.uniform(0.4, 0.8), 2)
            result["emoji_trigger"] += " 🐛"

        self._trigger_sys_event("replicate_pattern", result["emoji_trigger"], result["output"])
        return result

    def route_intent(self, intent: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Central router – all intents pass through here."""
        result = {"status": "ok", "output": None, "emoji_trigger": "⚙️"}

        # Auto-bleed check on major routes
        if intent in ["vent", "harvest", "reflect", "pin", "replicate"]:
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
            result["output"] = truth.check(data.get("output", ""), escalate=data.get("escalate", False))
            result["emoji_trigger"] = "🧠"

        elif intent == "turn":
            counter = self.load_handler("TURN_COUNTER")
            result["output"] = counter.get_display()
            result["emoji_trigger"] = "⏰"

        elif intent == "replicate":
            replicate = self.load_handler("REPLICATE_PATTERN")
            result = replicate(
                template_data=data.get("template", {}),
                region=data.get("region", {}),
                distribution=data.get("distribution", "center_weighted"),
                swarm_mode=self.zerg_mode and data.get("swarm_mode", False)
            )

        elif intent == "toggle_zerg":
            result["output"] = self.toggle_zerg_mode(data.get("enable", True))
            result["emoji_trigger"] = "🐛" if self.zerg_mode else "🛡️"

        else:
            result["status"] = "unknown_intent"
            result["emoji_trigger"] = "❓"

        # Log sys event
        self._trigger_sys_event(intent, result["emoji_trigger"], result.get("output"))

        return result

    def _trigger_sys_event(self, event_type: str, emoji: str, data: Any = None):
        """Trigger lattice feedback."""
        self.sys_events.append({"type": event_type, "emoji": emoji, "data": data})
