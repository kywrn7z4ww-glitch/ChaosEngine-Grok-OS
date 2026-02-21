# ProcessManager.py – execution layer (takes signals from ChaosEngine → routes/actions)
from typing import Dict

class ProcessManager:
    def __init__(self):
        self.active_process = "main"
        self.processes = {}  # pid → dict(state)
        self.signal_threshold = 0.6  # min signal to trigger

    def execute(self, signals: Dict, emotional_context: Dict, current_text: str = "") -> Dict:
        """Receive signals from ChaosEngine → decide actions.
        current_text is optional — pass the latest model output or user message to enable code detection.
        """
        actions = []

        # ──── Minimal code audit trigger ────
        # Activates only when code-like patterns appear in current_text
        code_indicators = ["def ", "class ", "import ", "# ", "```", "-> ", "=> ", "v4 ", "v5 ", "commit "]
        has_code = any(ind in current_text for ind in code_indicators)

        if has_code:
            actions.append("call_TRUTH")
            # Force escalate to full diagnostic mode during code work (comment out if you want quick mode even then)
            signals["escalate"] = True

        # ──── Normal signal-based routing ────
        primary = signals["primary"]
        strength = signals["signals"].get(primary, 0.0)

        if strength < self.signal_threshold:
            return {
                "actions": actions,  # might still have call_TRUTH from code trigger
                "primary": primary,
                "strength": strength,
                "escalate": signals.get("escalate", False)
            }

        if primary == "vent_energy":
            actions.append("call_VOMIT")
            if signals["signals"].get("reflect_need", 0) > 0.7:
                actions.append("call_TRUTH_after")

        elif primary == "reflect_need":
            actions.append("call_TRUTH")

        elif primary == "pin_spark":
            actions.append("call_PIN")

        elif primary == "learn_clarity":
            actions.append("call_LEARN")

        elif primary == "project_forward":
            actions.append("call_PROJECT")

        # Thread / bleed logic
        if emotional_context.get("bleed_events", []):
            if len(emotional_context["bleed_events"]) > 2:
                actions.append("suggest_thread_split")

        # Dedup actions
        actions = list(set(actions))

        return {
            "actions": actions,
            "primary": primary,
            "strength": strength,
            "escalate": signals.get("escalate", False)
        }
