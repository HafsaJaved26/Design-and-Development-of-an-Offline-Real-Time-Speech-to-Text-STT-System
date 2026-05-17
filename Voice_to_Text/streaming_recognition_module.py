# -*- coding: utf-8 -*-
"""
streaming_recognition_module.py - FIXED VERSION
Simplified to accumulate audio until STOP, then transcribe ALL audio at once.
This avoids Whisper's minimum audio length requirements.
"""

import time
import numpy as np

MIN_AUDIO_SAMPLES = 16000


class StreamingRecognitionModule:

    def __init__(self):
        self.model = None
        self.queue_manager = None
        self.partial_callback = None
        self.final_callback = None

        self.is_processing = False
        self.audio_buffer = []
        self.buffer_duration = 0.0
        self.is_stopping = False

        self.chunks_processed = 0
        self.partial_count = 0
        self.final_count = 0

    def set_recognizer(self, model):
        self.model = model

    def set_queue_manager(self, queue_object):
        self.queue_manager = queue_object

    def register_partial_callback(self, callback_function):
        self.partial_callback = callback_function

    def register_final_callback(self, callback_function):
        self.final_callback = callback_function

    def start_processing(self):
        """Main loop - just accumulate audio until STOP."""
        print("[Recognizer] >> START_PROCESSING")
        self.is_processing = True
        self.is_stopping = False
        self.audio_buffer = []
        self.buffer_duration = 0.0
        chunk_count = 0

        while self.is_processing:
            chunk = self.queue_manager.get_from_queue()
            
            if chunk is not None:
                chunk_count += 1
                if chunk_count <= 5 or chunk_count % 50 == 0:
                    print(f"[Audio] Got chunk {chunk_count} ({len(chunk)} bytes)")
                
                # Just accumulate
                self.audio_buffer.append(chunk)
                self.buffer_duration = len(b"".join(self.audio_buffer)) / (16000 * 2)
                self.chunks_processed += 1
            else:
                time.sleep(0.01)
        
        print(f"[Recognizer] Processing loop ended")

    def _prepare_audio(self, audio_bytes: bytes) -> np.ndarray:
        """Convert bytes to float32 normalized audio."""
        print(f"[Audio] Preparing {len(audio_bytes)} bytes...")
        
        # Convert to float32
        audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        
        # Normalize
        rms = np.sqrt(np.mean(audio_np**2))
        print(f"[Audio] RMS: {rms:.6f}, samples: {len(audio_np)}")
        
        if rms > 0.0001:
            target_rms = 0.1
            if rms < target_rms:
                gain = min(target_rms / rms, 10.0)
                audio_np = audio_np * gain
                audio_np = np.clip(audio_np, -1.0, 1.0)
                print(f"[Audio] Applied gain {gain:.2f}")
        
        return audio_np

    def _transcribe_buffer(self):
        """Transcribe all audio in buffer."""
        print(f"[Transcribe] Starting transcription ({len(self.audio_buffer)} chunks, {self.buffer_duration:.1f}s)")
        
        if not self.audio_buffer or not self.model:
            print("[Transcribe] ERROR: No buffer or model")
            return

        audio_bytes = b"".join(self.audio_buffer)
        print(f"[Transcribe] Total audio: {len(audio_bytes)} bytes")
        
        try:
            # Prepare audio
            audio_np = self._prepare_audio(audio_bytes)
            
            # Ensure minimum length for Whisper
            if len(audio_np) < 16000:
                print(f"[Transcribe] ERROR: Audio too short ({len(audio_np)} samples, need 16000+)")
                return
            
            print(f"[Transcribe] Calling Whisper.transcribe() with {len(audio_np)} samples...")
            
            # Call Whisper
            result = self.model.transcribe(
                audio_np,
                language="ur",
                fp16=False,
                task="transcribe",
                verbose=False,
                temperature=0.0,
            )
            
            text = (result.get("text", "") or "").strip()
            print(f"[Transcribe] ✓ Result: '{text}' ({len(text)} chars)")
            
            # Fire callback if we have text
            if text:
                print(f"[Callback] Firing final callback...")
                if self.final_callback:
                    try:
                        self.final_callback(text)
                        self.final_count += 1
                        print(f"[Callback] ✓ Stored (count: {self.final_count})")
                    except Exception as e:
                        print(f"[Callback] ✗ ERROR: {e}")
                else:
                    print("[Callback] ERROR: callback is None")
            else:
                print("[Transcribe] WARNING: Empty result from Whisper")
        
        except Exception as e:
            print(f"[ERROR Transcribe] {type(e).__name__}: {str(e)[:100]}")
            import traceback
            traceback.print_exc()

    def stop_processing(self) -> str:
        """Stop recording and transcribe all accumulated audio."""
        print(f"[Stop] >> stop_processing() - buffer: {len(self.audio_buffer)} chunks, {self.buffer_duration:.1f}s")
        
        self.is_stopping = True
        self.is_processing = False
        
        # Transcribe ALL audio
        if self.audio_buffer:
            print("[Stop] Transcribing accumulated audio...")
            self._transcribe_buffer()
        else:
            print("[Stop] No audio to transcribe")
        
        time.sleep(0.2)
        print(f"[Stop] << Done (stored {self.final_count} transcriptions)")
        return ""

    def _is_bad_text(self, text: str) -> bool:
        """Check if text is garbage."""
        text = (text or "").strip()
        if not text or text in (".", "..", "...", "sil"):
            return True
        if all(c in " .,،؟!۔\n" for c in text):
            return True
        return False

    def get_statistics(self) -> dict:
        return {
            "chunks_processed": self.chunks_processed,
            "partial_count": self.partial_count,
            "final_count": self.final_count,
        }
