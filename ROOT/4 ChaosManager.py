def route_intent(self, intent: str, data: Dict[str, Any] = None, caller: str = None) -> Dict[str, Any]:
    if data is None:
        data = {}
    result = {"status": "ok", "output": None, "emoji_trigger": "⚙️"}

    # Recursion & bleed guard (keep from before)
    if caller == "ZERG_SWARM" and "zerg" in intent.lower():
        return {"status": "veto", "output": "Swarm cannot spawn swarm"}

    # TOOL INTEGRATION – the new spine
    if "tool " in intent.lower() or intent.lower().startswith(("browse", "search", "execute", "code", "web", "x_search")):
        # Parse
        cmd = intent.lower().split()[0]
        arg = intent[len(cmd):].strip()

        if "browse" in cmd or "page" in cmd:
            # Example: browse https://raw.githubusercontent.com/... instructions=raw full
            # (in real use Grok will trigger the tool)
            result["output"] = f"[TOOL] browse_page called with: {arg}"
            result["emoji_trigger"] = "📦"
            # Real tool would be called here by Grok when user says the command

        elif "code" in cmd or "execute" in cmd:
            result["output"] = f"[TOOL] code_execution ready for: {arg}"
            result["emoji_trigger"] = "🧠"

        elif "search" in cmd or "web" in cmd:
            result["output"] = f"[TOOL] web_search: {arg}"
            result["emoji_trigger"] = "🔍"

        elif "x_" in cmd:
            result["output"] = f"[TOOL] X search: {arg}"
            result["emoji_trigger"] = "🐦"

        else:
            result["output"] = "Tool recognized but not wired yet – say exact: tool browse URL"
        return result

    # Existing zerg / load / route paths (keep your previous upgrades)
    # ... paste your current zerg parsing here ...

    self._trigger_sys_event(intent, result["emoji_trigger"], result.get("output"))
    if self.lattice:
        self.lattice.process_input(intent)

    return result
