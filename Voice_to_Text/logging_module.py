# -*- coding: utf-8 -*-
"""
logging_module.py
Member 8 (Hafsa Javed) — Logging Module
Saves all transcriptions to UTF-8 text files with structured headers/footers.
"""

import os
import datetime


class LoggingModule:
    """
    Creates per-session log files inside a logs/ directory.
    Each file contains a header, timestamped transcription lines, and a footer.
    Handles Urdu text correctly via UTF-8 encoding throughout.
    """

    def __init__(self):
        self.current_log_file = None
        self.log_file         = None   # open file handle

    # ── Directory management ──────────────────────────────────────────────────

    def ensure_log_directory(self):
        """Create the logs/ folder if it does not already exist."""
        if not os.path.exists("logs"):
            try:
                os.makedirs("logs")
                print("[Logger] Created logs/ directory.")
            except PermissionError:
                print("[Logger] ERROR: Cannot create logs/ — permission denied.")
            except OSError as e:
                print(f"[Logger] ERROR creating logs/: {e}")

    # ── File naming ───────────────────────────────────────────────────────────

    def generate_filename(self) -> str:
        """
        Generate a unique filename based on the current date and time.
        Example:  logs/transcript_20260302_153045.txt
        """
        now      = datetime.datetime.now()
        filename = f"transcript_{now.strftime('%Y%m%d_%H%M%S')}.txt"
        return os.path.join("logs", filename)

    # ── Session lifecycle ─────────────────────────────────────────────────────

    def start_session(self):
        """
        Open a new log file and write the session header.
        Called by SessionController at the start of each session.
        """
        self.ensure_log_directory()
        self.current_log_file = self.generate_filename()

        try:
            self.log_file = open(self.current_log_file, "w", encoding="utf-8")
            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log_file.write("========================================\n")
            self.log_file.write(f"Session started: {now_str}\n")
            self.log_file.write("========================================\n\n")
            self.log_file.flush()
            print(f"[Logger] Log file opened: {self.current_log_file}")

        except PermissionError:
            print(f"[Logger] ERROR: Permission denied writing to {self.current_log_file}")
        except OSError as e:
            print(f"[Logger] ERROR opening log file: {e}")

    def log_transcription(self, timestamp: str, text: str):
        """
        Write a single transcription line immediately to disk.
        Called by FinalResultHandler for every completed sentence.
        """
        if self.log_file is None:
            return
        try:
            self.log_file.write(f"[{timestamp}] {text}\n")
            self.log_file.flush()          # write-through so data is never lost
        except OSError as e:
            print(f"[Logger] ERROR writing transcription: {e}")

    def end_session(self, duration: float, sentence_count: int) -> str:
        """
        Write the session footer and close the log file.
        Returns the log file path for display in the UI.
        """
        if self.log_file is None:
            return self.current_log_file or ""

        try:
            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log_file.write("\n----------------------------------------\n")
            self.log_file.write(f"Session ended: {now_str}\n")
            self.log_file.write(f"Total sentences: {sentence_count}\n")
            self.log_file.write(f"Processing time: {duration:.1f} seconds\n")
            self.log_file.write("========================================\n")
            print(f"[Logger] Session closed — {sentence_count} sentences — {self.current_log_file}")

        except OSError as e:
            print(f"[Logger] ERROR writing session footer: {e}")
        
        finally:
            try:
                if self.log_file is not None:
                    self.log_file.close()
                    self.log_file = None
            except OSError as e:
                print(f"[Logger] ERROR closing log file: {e}")

        return self.current_log_file or ""

    # ── Accessor ──────────────────────────────────────────────────────────────

    def get_logger_function(self):
        """Return log_transcription as a callable for FinalResultHandler."""
        return self.log_transcription

    def get_current_log_file(self) -> str:
        """Return the path to the current (or most recent) log file."""
        return self.current_log_file or ""
