# python/python-process-lib/sys_mgr.py
# ⚙️ v1.1 – System Manager (reads SYS_HEALTH, suggests fixes)

from typing import Dict

class SystemManager:
    def __init__(self, sys_health):
        self.sys_health = sys_health  # instance of SystemHealth class

    def check_and_suggest(self) -> str:
        """Read metrics from SYS_HEALTH, suggest most relevant fix."""
        metrics = self.sys_health.metrics
        score = self.sys_health.get_health_score()

        emoji = "✅" if score >= 85 else "⚠️" if score >= 60 else "‼️"
        report = f"⚙️ SYS_MGR Health: {emoji} {int(score)}%"

        issues = []

        if metrics.get('decay_bias', 0) > 1.4:
            issues.append(("decay rising", "/reanchor (pull /root + /storage)"))

        if metrics.get('node_count', 0) > 80 or metrics.get('storage_size', 0) > 25:
            issues.append(("bloat high", "/🗑️ prune"))

        if metrics.get('loop_count', 0) > 4:
            issues.append(("loop/repeat", "/thread split or /vent"))

        if metrics.get('frustr', 0) > 0.6 or metrics.get('ache', 0) > 0.6:
            issues.append(("emotion spike", "/vent or /clarity"))

        if metrics.get('bleed_score', 0) > 0.35:
            issues.append(("bleed detected", "/thread split or /clarity"))

        if issues:
            # Suggest top one (highest penalty first)
            issues.sort(key=lambda x: 100 - score, reverse=True)
            top_issue, top_fix = issues[0]
            report += f" – {top_issue} – {top_fix}"

        return report