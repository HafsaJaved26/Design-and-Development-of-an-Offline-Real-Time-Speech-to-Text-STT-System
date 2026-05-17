# -*- coding: utf-8 -*-
"""
partial_result_manager.py
Member 6 (Faraz Khan) — Partial Result Manager
Manages live partial transcription updates for the UI.
"""

import threading


class PartialResultManager:
    """
    Receives partial recognition results from StreamingRecognitionModule
    and makes the current live text available to SessionController / UI.
    Also provides a clear function that FinalResultHandler calls when
    a sentence is complete.
    """

    def __init__(self):
        self.current_partial = ""   # most recent partial text from Vosk
        self.last_partial    = ""   # last value dispatched to display
        self.update_count    = 0    # how many unique updates received
        self.clear_count     = 0    # how many times display was cleared
        self._lock           = threading.Lock()  # thread-safe access

    # ── Called by StreamingRecognitionModule ──────────────────────────────────

    def update_partial(self, partial_text: str) -> bool:
        """
        Store new partial text.
        Returns True if the text has changed (UI should refresh), False otherwise.
        """
        with self._lock:
            self.current_partial = partial_text

            if self.current_partial != self.last_partial:
                self.last_partial = self.current_partial
                self.update_count += 1
                print(f"[Partial] updated to: '{partial_text}'")
                return True

            return False

    # ── Called by SessionController / UI ─────────────────────────────────────

    def get_current_partial(self) -> str:
        """Return the most recent partial transcription text."""
        with self._lock:
            return self.current_partial

    # ── Called by FinalResultHandler ─────────────────────────────────────────

    def clear_for_final(self):
        """
        Reset partial buffers when a final sentence has been recognised.
        Called by FinalResultHandler so the live box clears between sentences.
        """
        with self._lock:
            self.current_partial = ""
            self.last_partial    = ""
            self.clear_count    += 1

    # ── Callback accessors (for SessionController wiring) ────────────────────

    def get_callback_for_member5(self):
        """Return the update_partial method as a callback for StreamingRecognitionModule."""
        return self.update_partial

    def get_clear_function(self):
        """Return the clear_for_final method as a callback for FinalResultHandler."""
        return self.clear_for_final

    # ── Statistics ────────────────────────────────────────────────────────────

    def get_statistics(self) -> dict:
        """Return update and clear counters."""
        return {
            "update_count": self.update_count,
            "clear_count":  self.clear_count,
        }
