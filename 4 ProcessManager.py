# ProcessManager.py – execution layer (takes signals from ChaosEngine → routes/actions)

from typing import Dict

class ProcessManager:
    def __init__(self):
        self.active_process = "main"
        self.processes = {}  # pid → dict(state)
        self.signal_threshold = 0.6  # min signal to trigger

    def execute(self, signals: Dict, emotional_context: Dict):
        """Receive signals from ChaosEngine → decide actions"""
        primary = signals["primary"]
        strength = signals["signals"].get(primary, 0.0)
        
        if strength < self.signal_threshold:
            return {"action": "none", "message": "signal too weak — clarify?"}
        
        actions = []
        
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
        if emotional_context.get("bleed_events", []):  # example
            if len(emotional_context["bleed_events"]) > 2:
                actions.append("suggest_thread_split")
        
        return {
            "actions": actions,
            "primary": primary,
            "strength": strength
        }
