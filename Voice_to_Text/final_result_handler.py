# -*- coding: utf-8 -*-
"""
final_result_handler.py
Member 7 (Abdul Jabbar) — Final Result Handler
FIXED: thread safety aur duplicate filter
"""

import datetime
import threading


class FinalResultHandler:

    def __init__(self):
        self.all_transcriptions = []
        self.sentence_count     = 0
        self.clear_function     = None
        self.logger_function    = None
        self.session_start_time = None
        self.session_end_time   = None
        self._lock              = threading.Lock()
        # ✅ FIX: duplicate sentence filter
        self.last_text          = ""

    def handle_final(self, final_text: str):
        print(f"[FinalHandler] handle_final() called with text: '{final_text}'")
        
        if not final_text or not final_text.strip():
            print("[FinalHandler] Empty text, returning")
            return

        final_text = final_text.strip()

        # ✅ FIX: same text dobara mat add karo
        if final_text == self.last_text:
            print(f"[FinalHandler] Duplicate skipped: '{final_text[:40]}'")
            return

        self.last_text = final_text
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        if self.clear_function is not None:
            self.clear_function()

        print(f"✅ [{timestamp}] {final_text}")

        with self._lock:
            entry = {"timestamp": timestamp, "text": final_text}
            self.all_transcriptions.append(entry)
            self.sentence_count += 1
            print(f"[FinalHandler] Stored transcription. Total count: {self.sentence_count}")

        if self.logger_function is not None:
            self.logger_function(timestamp, final_text)

    def handle_no_speech(self):
        print("  ⚠  No speech detected in this segment.")

    def get_callback_for_member5(self):
        return self.handle_final

    def set_clear_function(self, clear_func):
        self.clear_function = clear_func

    def set_logger_function(self, log_func):
        self.logger_function = log_func

    def set_session_start(self, start_time: float):
        self.session_start_time = start_time

    def set_session_end(self, end_time: float):
        self.session_end_time = end_time

    def get_all_transcriptions(self) -> list:
        with self._lock:
            result = self.all_transcriptions.copy()
            print(f"[FinalHandler.get_all_transcriptions()] Returning {len(result)} transcriptions")
            if result:
                for item in result:
                    print(f"  - {item}")
            return result

    def get_sentence_count(self) -> int:
        with self._lock:
            return self.sentence_count

    def get_session_summary(self) -> dict:
        with self._lock:
            return {
                "total_sentences": self.sentence_count,
                "transcriptions":  self.all_transcriptions.copy(),
                "session_start":   self.session_start_time,
                "session_end":     self.session_end_time,
            }