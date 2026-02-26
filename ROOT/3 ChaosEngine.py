def route_intent(self, intent: str, data: Dict[str, Any] = None, caller: str = None) -> Dict[str, Any]:
    if data is None:
        data = {}
    result = {"status": "ok", "output": None, "emoji_trigger": "⚙️"}

    # Recursion guard
    if caller == "ZERG_SWARM" and intent.startswith("zerg"):
        return {"status": "recursion_blocked", "output": "Swarm cannot call swarm – vetoed"}

    # Bleed/vibe quick check before routing
    if self.lattice and (self.lattice.nodes.get("frustration", 0) > 0.7 or self.lattice.nodes.get("ache", 0) > 0.7):
        result["emoji_trigger"] = "🩸"
        result["output"] = "[QUEEN INTERRUPT] Bleed spike. Clarify or vent first?"
        return result

    # Smart intent parser
    words = intent.lower().split()
    if words[0].startswith("/"):
        cmd = words[0][1:]
        args = " ".join(words[1:])
        if cmd == "zerg":
            swarm = self.load_handler("ZERG_SWARM")
            if swarm:
                sub = words[1] if len(words) > 1 else None
                if sub == "activate":
                    result["output"] = swarm.activate(args)
                    result["emoji_trigger"] = "👑"
                elif sub == "spawn":
                    vibe = words[2] if len(words) > 2 else "auto"
                    result["output"] = swarm.spawn(vibe)
                    result["emoji_trigger"] = "🐛"
                elif sub == "toggle":
                    enable = "true" in args.lower()
                    result["output"] = swarm.toggle(enable)
                    result["emoji_trigger"] = "Zerg" if enable else "Shield"
        elif cmd == "load_handler":
            name = args.strip()
            handler = self.load_handler(name)
            result["output"] = f"Loaded {name}" if handler else f"Failed to load {name}"
            result["emoji_trigger"] = "📦"
        elif cmd == "route":
            # recursive safe call
            sub_intent = " ".join(words[1:])
            return self.route_intent(sub_intent, caller="user")
        else:
            result["status"] = "unknown_cmd"
    else:
        # fallback natural language → try swarm first if vibe high
        swarm = self.load_handler("ZERG_SWARM")
        if swarm and self.lattice and self.lattice.nodes.get("spark", 0) > 0.5:
            result["output"] = swarm.activate(intent)
            result["emoji_trigger"] = "👑"
        else:
            result["status"] = "unknown_intent"

    # Trigger sys event & pipe back to lattice
    self._trigger_sys_event(intent, result["emoji_trigger"], result.get("output"))
    if self.lattice:
        self.lattice.process_input(intent)  # warm lattice

    return result
