#!/usr/bin/env python3
"""
chaos-engine.py — Grok OS ChaosEngine v3.0 (Full Skill Manager)
Purpose: Central brain that handles loading, routing, remote installation,
skill chaining, dynamic discovery, and live indexing.

Combines the solid original design with new remote + chaining features.
"""

import importlib.util
import json
import os
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Set

# =============================================================================
# CONFIG
# =============================================================================
REPO_OWNER = "kywrn7z4ww-glitch"
REPO_NAME = "ChaosEngine-Grok-OS"
BRANCH = "main"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/ROOT/"

LOCAL_ROOT = Path("/home/workdir/artifacts/grok-os/ROOT")
CACHE_DIR = Path("/home/workdir/artifacts/grokos/.cache")
INDEX_CACHE = CACHE_DIR / "chaos_live_index.json"

PROCESS_DIRS = ["PROCESS", "layers", "skills", "chaos_engine", "emotion-net"]

POISON_PILLS = ["readme.md", "tetris_curse.py"]


class ChaosEngine:
    def __init__(self):
        self.turn = None
        self.emotionnet = None
        self.processes: Dict[str, Any] = {}
        self.active_layer: str = "dev"
        self.live_index: Set[str] = set()

        self._load_emotionnet()
        self._build_live_index()
        self._load_all_processes_dynamically()

        print("⚙️  ChaosEngine v3.0 — Full Skill Manager Online (≥99% confidence)")

    # -------------------------------------------------------------------------
    # INDEX & DISCOVERY
    # -------------------------------------------------------------------------
    def _build_live_index(self):
        """Dynamically scan all subfolders and build live index"""
        print("🔍 Building live skill/process index...")
        self.live_index = set()

        for base_dir in PROCESS_DIRS:
            base_path = LOCAL_ROOT / base_dir
            if not base_path.exists():
                continue
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    if file.endswith(".py") and not file.startswith("__"):
                        rel_path = os.path.relpath(os.path.join(root, file), LOCAL_ROOT)
                        if not any(p in rel_path.lower() for p in POISON_PILLS):
                            self.live_index.add(rel_path)

        # Save index (guarded against I/O errors in restricted environments)
        try:
            index_data = {
                "timestamp": datetime.now().isoformat(),
                "count": len(self.live_index),
                "files": sorted(list(self.live_index)),
            }
            INDEX_CACHE.parent.mkdir(parents=True, exist_ok=True)
            INDEX_CACHE.write_text(json.dumps(index_data, indent=2))
            print(f"  ✅ Live index built ({len(self.live_index)} files)")
        except Exception as e:
            print(f"  ⚠️  Index cache write skipped: {e}")

    # -------------------------------------------------------------------------
    # LOADING
    # -------------------------------------------------------------------------
    def _load_emotionnet(self):
        try:
            filepath = (
                LOCAL_ROOT / "emotion-net/emotion_net.py"
            )  # fixed to actual filename
            if not filepath.exists():
                print("⚠️  emotion_net.py not found")
                return
            spec = importlib.util.spec_from_file_location("EmotionNet", filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.emotionnet = module.EmotionNet()
            print("🧠 EmotionNet loaded")
        except Exception as e:
            print(f"⚠️  Could not load EmotionNet: {e}")

    def _load_all_processes_dynamically(self):
        """Load all discovered .py files"""
        print("🔄 Loading all discovered processes...")
        loaded = 0
        for rel_path in sorted(self.live_index):
            if not rel_path.endswith(".py"):
                continue
            try:
                full_path = LOCAL_ROOT / rel_path
                module_name = Path(rel_path).stem
                spec = importlib.util.spec_from_file_location(module_name, full_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                handler = None
                if hasattr(module, module_name):
                    handler = getattr(module, module_name)()
                elif hasattr(module, "main"):
                    handler = module
                else:
                    handler = module

                self.processes[module_name.lower()] = handler
                loaded += 1
            except Exception as e:
                print(f"  ❌ Failed to load {rel_path}: {e}")

        print(f"✅ Loaded {loaded} processes/skills dynamically")

    # -------------------------------------------------------------------------
    # REMOTE SKILL INSTALLATION (Downloader)
    # -------------------------------------------------------------------------
    def install_remote_skill(self, skill_path: str, auto_trust: bool = False) -> bool:
        """Fetch and install a skill from our repo (or ask for unknown sources)"""
        if not auto_trust and "kywrn7z4ww-glitch/ChaosEngine-Grok-OS" not in skill_path:
            confirm = input(
                f"Install skill from unknown source? (y/n): {skill_path} "
            ).lower()
            if confirm != "y":
                print("  ❌ Installation cancelled")
                return False

        url = RAW_BASE + skill_path
        local_path = LOCAL_ROOT / skill_path
        local_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                content = resp.read()
            local_path.write_bytes(content)
            print(f"  ✅ Installed remote skill: {skill_path}")
            self._build_live_index()  # Refresh index
            return True
        except Exception as e:
            print(f"  ❌ Failed to install {skill_path}: {e}")
            return False

    # -------------------------------------------------------------------------
    # ROUTING
    # -------------------------------------------------------------------------
    def _calculate_confidence(self, intent: str) -> float:
        base = 75.0
        if intent.startswith("/"):
            base += 15
        if self.emotionnet:
            pass  # Future: use real emotional state
        return min(100.0, base)

    def route_intent(self, intent: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        if data is None:
            data = {}

        confidence = self._calculate_confidence(intent)

        if self.active_layer == "void":
            return {"status": "ok", "output": None, "inline_handoff": "🔇"}

        if confidence >= 99:
            cmd = intent[1:].split()[0] if intent.startswith("/") else "sys_health"
            handler = self.processes.get(cmd.lower())
            if handler:
                result = (
                    handler.process(data) if hasattr(handler, "process") else handler
                )
                return {"status": "executed", "process": cmd, "result": result}
            else:
                return {"status": "unknown_command", "command": cmd}

        return {
            "status": "clarify",
            "message": f"Confidence {confidence:.1f}% — DISCUSS CLARITY required",
            "suggestions": [
                "Run /help",
                "Try /dev for debugging",
                "Use /casual for general chat",
            ],
        }

    # -------------------------------------------------------------------------
    # SKILL CHAINING (Chainfire Logic)
    # -------------------------------------------------------------------------
    def chain_skills(
        self, skill_list: list, data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Run multiple skills in sequence, passing data between them"""
        if data is None:
            data = {}

        results = []
        for skill_name in skill_list:
            handler = self.processes.get(skill_name.lower())
            if handler:
                try:
                    result = (
                        handler.process(data)
                        if hasattr(handler, "process")
                        else handler
                    )
                    results.append({"skill": skill_name, "result": result})
                    if isinstance(result, dict):
                        data.update(result)  # Pass data forward
                except Exception as e:
                    results.append({"skill": skill_name, "error": str(e)})
            else:
                results.append({"skill": skill_name, "error": "Not found"})

        return {"status": "chained", "results": results}

    # -------------------------------------------------------------------------
    # UTILITIES
    # -------------------------------------------------------------------------
    def set_layer(self, layer: str):
        self.active_layer = layer.lower()
        print(f"📍 Layer switched to: /{self.active_layer}")

    def load_agent(self, name: str) -> str:
        try:
            from STORAGE.AGENTS.AGENT_LOADER import load_agent

            return load_agent(name)
        except:
            return f"⚠️ Agent loader not available"

    def list_agents(self) -> list:
        try:
            from STORAGE.AGENTS.AGENT_LOADER import list_all_agents

            return list_all_agents()
        except:
            return []

    def load_all(self):
        print("🔄 ChaosEngine fully initialized with live index")
        return "Ready — all skills and processes loaded"


# Quick self-test
if __name__ == "__main__":
    engine = ChaosEngine()
    engine.load_all()
    print(engine.route_intent("/boot"))
    print(engine.route_intent("check system health"))


# ============================================================
# CHAIN-FIRE MODE: Module-level singleton for package __init__.py
# ============================================================
chaos_engine = None
try:
    chaos_engine = ChaosEngine()
except Exception as e:
    # Improved error handling for chain-fire (prevents I/O errors on cache/log writes)
    print(f"[ChaosEngine] ⚠️  Chain-fire init deferred: {e}")
    # Still allow partial use if core components loaded
    if "EmotionNet" in str(e) or "cache" in str(e).lower():
        print(
            "  → Continuing with limited functionality (EmotionNet may still be available)"
        )
