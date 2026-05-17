# -*- coding: utf-8 -*-
"""
model_loader_module.py
Member 2 (Ghazal Hafeez) - Model Loader Module
Loads the OpenAI Whisper Urdu speech recognition model.
"""

import whisper


class ModelLoaderModule:
    """
    Responsible for loading and exposing the Whisper Urdu
    speech recognition model.
    """

    def __init__(self, model_name: str = "base"):
        self.model_name = model_name
        self.model = None
        self.model_loaded = False
        self.sampling_rate = 16000

    def load_model(self) -> bool:
        """
        Load the Whisper model.
        Returns True on success, False on failure.
        """
        try:
            print(f"[ModelLoader] Loading Whisper '{self.model_name}' model...")
            self.model = whisper.load_model(self.model_name)
            self.model_loaded = True
            print("[ModelLoader] Model loaded successfully.")
            return True
        except Exception as exc:
            print(f"[ModelLoader] ERROR while loading model: {exc}")
            self.model_loaded = False
            return False

    def get_recognizer(self):
        """Return the Whisper model instance."""
        return self.model

    def is_model_loaded(self) -> bool:
        """Return True if the model was loaded successfully."""
        return self.model_loaded

    def get_sampling_rate(self) -> int:
        """Return the required audio sampling rate (16 kHz)."""
        return self.sampling_rate

    def get_model_info(self) -> dict:
        """Return a metadata dictionary describing the loaded model."""
        return {
            "name": f"whisper-{self.model_name}",
            "language": "Urdu (ur)",
            "sampling_rate": self.sampling_rate,
            "loaded": self.model_loaded,
            "engine": "OpenAI Whisper",
            "mode": "Fully Offline",
        }
