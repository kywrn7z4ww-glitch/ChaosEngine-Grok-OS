#!/usr/bin/env python3
"""
response_pipeline.py — Response Pipeline v1.0
Purpose: Full input → output flow for Grok OS.
Connects: User Input → ChaosEngine → LayerManager → UI Manager → Formatted Output
"""

from typing import Optional, Dict, Any

# Import our components
from chaos_engine import ChaosEngine
from layer_manager import layer_manager, get_current_layer
from ui_manager import format_output


class ResponsePipeline:
    def __init__(self):
        self.chaos_engine = ChaosEngine()
        self.turn = 0

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
