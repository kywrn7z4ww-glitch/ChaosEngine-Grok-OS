# python/python-process-lib/sys_mgr.py
# v1 – ⚙️ System Manager (session health, fault detection, maintenance nudges)

class SystemManager:
    def __init__(self):
        self.health_score = 100.0
        self.metrics = {}  # populated on check

    def check_health(self,
                     decay_bias: float,
                     node_count: int,
                     frustr: float,
                     ache: float,
                     loop_count: int,
                     storage_size: int,
                     bleed_detected: bool = False) -> str:
        """Run health check – called on trigger or auto-nudge."""
        self.metrics = {
            'decay_bias': decay_bias,
            'node_count': node_count,
            'frustr': frustr,
            'ache': ache,
            'loop_count': loop_count,
            'storage_size': storage_size,
            'bleed': bleed_detected
        }

        score = 100.0
        if decay_bias > 1.5: score -= 25
        if node_count > 100: score -= 20
        if frustr > 0.6 or ache > 0.6: score -= 15
        if loop_count > 4: score -= 20
        if storage_size > 25: score -= 15
        if bleed_detected: score -= 10
        score = max(0, score)
        self.health_score = score

        emoji = "✅" if score >= 85 else "⚠️" if score >= 60 else "‼️"
        report = f"⚙️ SYS_MGR Health: {emoji} {int(score)}%"

        if score < 85:
            nudges = []
            if decay_bias > 1.5: nudges.append("/reanchor")
            if node_count > 100 or storage_size > 25: nudges.append("/🗑️ prune")
            if frustr > 0.6 or ache > 0.6: nudges.append("vent or /thread split")
            if loop_count > 4: nudges.append("/thread split or /prune")
            if bleed_detected: nudges.append("/clarity or vent")
            if nudges:
                report += f" – {', '.join(nudges)}"

        return report

    def auto_nudge(self) -> str:
        """Passive check – only returns nudge if critical."""
        if self.health_score < 70:
            return "⚙️ Nudge: Health low – /⚙️ for details"
        return ""

# Usage in sim:
# mgr = SystemManager()
# print(mgr.check_health(decay_bias=1.2, node_count=65, frustr=0.4, ache=0.3, loop_count=1, storage_size=12, bleed_detected=False))
# → "⚙️ SYS_MGR Health: ✅ 100%"
