# -*- coding: utf-8 -*-
"""
session_controller.py
Member 9 (M. Zaheer) — System Integration & Session Controller
"""

import sys
import time
import threading
import logging

from initialization_module        import InitializationModule
from model_loader_module          import ModelLoaderModule
from audio_input_module           import AudioInputModule
from audio_queue_manager_module   import AudioQueueManagerModule
from streaming_recognition_module import StreamingRecognitionModule
from partial_result_manager       import PartialResultManager
from final_result_handler         import FinalResultHandler
from logging_module               import LoggingModule

_log = logging.getLogger("SessionController")
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(name)s] %(levelname)s — %(message)s",
    datefmt="%H:%M:%S",
)


class SessionController:

    def __init__(self):
        _log.info("Initialising SessionController…")

        self.init_module = InitializationModule()
        if not self.init_module.validate_initialization():
            _log.critical("InitializationModule validation failed — aborting.")
            sys.exit(1)
        _log.debug("Step 1 ✓  InitializationModule ready")

        # ✅ base model — real-time fast results
        self.model_loader = ModelLoaderModule("base")
        _log.info("Loading Whisper model — please wait…")
        if not self.model_loader.load_model():
            _log.critical("FATAL: Whisper model failed to load.")
            sys.exit(1)
        _log.debug("Step 2 ✓  Model loaded — %s", self.model_loader.get_model_info())

        self.queue_manager = AudioQueueManagerModule(max_size=200)
        _log.debug("Step 3 ✓  AudioQueueManagerModule ready")

        self.audio_input = AudioInputModule()
        self.audio_input.set_queue_manager(self.queue_manager)
        _log.debug("Step 4 ✓  AudioInputModule connected to queue")

        self.recognizer_module = StreamingRecognitionModule()
        self.recognizer_module.set_recognizer(self.model_loader.get_recognizer())
        self.recognizer_module.set_queue_manager(self.queue_manager)
        _log.debug("Step 5 ✓  StreamingRecognitionModule connected")

        self.partial_manager = PartialResultManager()
        self.final_handler   = FinalResultHandler()
        _log.debug("Step 6 ✓  PartialResultManager & FinalResultHandler created")

        self.recognizer_module.register_partial_callback(
            self.partial_manager.update_partial
        )
        self.recognizer_module.register_final_callback(
            self.final_handler.handle_final
        )
        self.final_handler.set_clear_function(
            self.partial_manager.clear_for_final
        )
        _log.debug("Step 7 ✓  Callbacks wired")

        self.logger = LoggingModule()
        self.logger.ensure_log_directory()
        _log.debug("Step 8 ✓  LoggingModule ready")

        self.final_handler.set_logger_function(self.logger.log_transcription)
        _log.debug("Step 9 ✓  Logger connected to FinalResultHandler")

        self.is_listening       = False
        self.processing_thread  = None
        self.session_start_time = None

        _log.info("✓ SessionController fully initialised — ready.")

    def start_session(self) -> bool:
        if self.is_listening:
            _log.warning("start_session() called while already listening — ignored.")
            return False

        _log.info("Starting new session…")
        self.init_module.reset_for_new_session()
        self.session_start_time = time.time()
        self.final_handler.set_session_start(self.session_start_time)
        self.logger.start_session()

        ok = self.audio_input.start_capture()
        if not ok:
            _log.error("Microphone capture failed — session aborted.")
            return False

        self.processing_thread = threading.Thread(
            target=self.recognizer_module.start_processing,
            name="RecognitionThread",
            daemon=True,
        )
        self.processing_thread.start()
        self.is_listening = True
        self.init_module.set_listening_state(True)
        _log.info("Session started — listening for Urdu speech.")
        return True

    def stop_session(self) -> str:
        """Stop recording and return the transcribed text."""
        if not self.is_listening:
            _log.warning("stop_session() called while not listening — ignored.")
            return ""

        _log.info("Stopping session…")
        self.is_listening = False
        self.init_module.set_listening_state(False)

        audio_stats = self.audio_input.stop_capture()
        _log.debug("Audio stopped — %s", audio_stats)

        # Tell recognizer to do final transcription
        _log.info("Calling recognizer stop_processing()...")
        self.recognizer_module.stop_processing()

        # Wait for recognition thread to finish
        if self.processing_thread and self.processing_thread.is_alive():
            _log.info("Waiting for recognition thread...")
            self.processing_thread.join(timeout=15.0)

        # ✅ Get ALL transcriptions that were stored (including final one)
        all_texts = self.final_handler.get_all_transcriptions()
        final_text = ""
        if all_texts:
            # Return the LATEST transcription
            final_text = all_texts[-1].get("text", "")
            _log.info(f"Got final text: '{final_text}'")

        duration = time.time() - self.session_start_time
        self.final_handler.set_session_end(time.time())
        self.init_module.update_time_tracker(
            self.session_start_time, self.session_start_time + duration
        )

        sentence_count = self.final_handler.get_sentence_count()
        log_path = self.logger.end_session(duration, sentence_count)

        _log.info(
            "Session ended — duration=%.1fs  sentences=%d  log=%s",
            duration, sentence_count, log_path,
        )
        
        # ✅ Return the final text
        return final_text

    def get_status(self) -> bool:
        return self.is_listening

    def get_partial_text(self) -> str:
        return self.partial_manager.get_current_partial()

    def get_all_transcriptions(self) -> list:
        return self.final_handler.get_all_transcriptions()

    def get_sentence_count(self) -> int:
        return self.final_handler.get_sentence_count()

    def get_session_duration(self) -> float:
        if self.is_listening and self.session_start_time:
            return time.time() - self.session_start_time
        return 0.0

    def get_log_file(self) -> str:
        return self.logger.get_current_log_file() or ""

    def get_queue_stats(self) -> dict:
        return self.queue_manager.get_statistics()

    def get_recognition_stats(self) -> dict:
        return self.recognizer_module.get_statistics()

    def get_model_info(self) -> dict:
        return self.model_loader.get_model_info()