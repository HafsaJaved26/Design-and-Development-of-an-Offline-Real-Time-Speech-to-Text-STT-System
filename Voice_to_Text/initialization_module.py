# -*- coding: utf-8 -*-
"""
initialization_module.py
Member 1 (Eman Afzal) — Initialization Module
Sets up all shared system variables used by other modules.
"""


class InitializationModule:
    """
    Foundation module that holds all shared state variables
    for the Urdu Speech-to-Text pipeline.
    """

    def __init__(self):
        # Is the system currently recording from the microphone?
        self.listening_state = False

        # Buffer for incoming audio chunks (filled by AudioQueueManager)
        self.audio_data_queue = []

        # All final recognised sentences for this session
        self.transcription_storage = []

        # Total elapsed time for the current recording session (seconds)
        self.processing_time_tracker = 0.0

        # Reference to the log file handler (set by LoggingModule)
        self.log_file_handler = None

        # Live partial text while the user is still speaking
        self.partial_result_buffer = ""

    # ── Core helpers ──────────────────────────────────────────────────────────

    def get_all_variables(self) -> dict:
        """Return all state variables as a dictionary."""
        return {
            "listening_state":        self.listening_state,
            "audio_data_queue":       self.audio_data_queue,
            "transcription_storage":  self.transcription_storage,
            "processing_time_tracker":self.processing_time_tracker,
            "log_file_handler":       self.log_file_handler,
            "partial_result_buffer":  self.partial_result_buffer,
        }

    def reset_for_new_session(self):
        """Clear all session data so a fresh session can begin."""
        self.transcription_storage   = []
        self.processing_time_tracker = 0.0
        self.partial_result_buffer   = ""
        self.listening_state         = False

    # ── Listening state ───────────────────────────────────────────────────────

    def set_listening_state(self, state: bool):
        """Update whether the system is currently recording."""
        self.listening_state = bool(state)

    def get_listening_state(self) -> bool:
        """Return the current listening state."""
        return self.listening_state

    # ── Time tracker ─────────────────────────────────────────────────────────

    def update_time_tracker(self, start_time: float, end_time: float):
        """Calculate and store session duration from two epoch timestamps."""
        self.processing_time_tracker = end_time - start_time

    # ── Validation ────────────────────────────────────────────────────────────

    def validate_initialization(self) -> bool:
        """
        Verify all required attributes exist and are correctly typed.
        Returns True on success, prints an error and returns False otherwise.
        """
        checks = [
            ("listening_state",         bool),
            ("audio_data_queue",        list),
            ("transcription_storage",   list),
            ("processing_time_tracker", float),
            ("partial_result_buffer",   str),
        ]
        for attr, expected_type in checks:
            if not hasattr(self, attr):
                print(f"[InitializationModule] ERROR: missing attribute '{attr}'")
                return False
            if not isinstance(getattr(self, attr), expected_type):
                print(
                    f"[InitializationModule] ERROR: '{attr}' should be "
                    f"{expected_type.__name__}, got "
                    f"{type(getattr(self, attr)).__name__}"
                )
                return False
        return True
