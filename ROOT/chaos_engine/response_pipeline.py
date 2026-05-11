#!/usr/bin/env python3
"""
response_pipeline.py — Response Pipeline v1.1
Purpose: Full input → output flow for Grok OS.
Connects: User Input → ChaosEngine → LayerManager → UI Manager → Formatted Output
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

# Use configurable root (same pattern as other files)
LOCAL_ROOT = Path(os.getenv("GROKOS_ROOT", "/home/workdir/artifacts/grok-os/ROOT"))

# Import from the package (uses singleton)
from chaos_engine import chaos_engine
from layer_manager import get_current_layer, layer_manager
from ui_manager import format_output


class ResponsePipeline:
    def __init__(self):
        # Use the existing singleton instead of creating a new one
        self.chaos_engine = chaos_engine
        self.turn = 1

    def process_input(self, user_input: str, data: Optional[Dict] = None) -> str:
        """Main entry point — processes user input and returns formatted output"""
        self.turn += 1

        if data is None:
            data = {}

        # Step 1: Route through ChaosEngine
        result = self.chaos_engine.route_intent(user_input, data)

        if result.get("status") != "executed":
            # Handle non-executed cases (clarify, error, etc.)
            raw_output = result.get("message", "Unknown response")
            layer = get_current_layer()
            return format_output(raw_output, layer, self.turn)

        # Step 2: Get raw output from the executed process
        raw_output = str(result.get("result", ""))

        # Step 3: Get current layer
        layer = get_current_layer()

        # Step 4: Format through UI Manager
        formatted_output = format_output(raw_output, layer, self.turn)

        return formatted_output


# Global instance
response_pipeline = ResponsePipeline()


def process_input(user_input: str, data: Optional[Dict] = None) -> str:
    """Convenience function for external use"""
    return response_pipeline.process_input(user_input, data)
