# -*- coding: utf-8 -*-
"""
audio_input_module.py
Member 3 (Eiman Zahra Awan) — Audio Input Module
FIXED: always prefer Realtek/actual mic over Sound Mapper
"""

import pyaudio
import numpy as np
from scipy.signal import resample_poly


class AudioInputModule:

    FORMAT   = pyaudio.paInt16
    CHANNELS = 1
    RATE     = 16000
    CHUNK_MS = 250

    def __init__(self):
        self.queue_manager = None
        self.chunk_count   = 0
        self.byte_count    = 0
        self.is_capturing  = False
        self.device_index  = None
        self.input_rate    = None
        self.chunk_size    = None

        self._pyaudio_instance = None
        self._stream           = None

    def set_queue_manager(self, queue_object):
        self.queue_manager = queue_object

    def initialize_microphone(self) -> bool:
        self._pyaudio_instance = pyaudio.PyAudio()
        info     = self._pyaudio_instance.get_host_api_info_by_index(0)
        num_devs = info.get("deviceCount", 0)

        found   = False
        chosen  = None
        chosen_name = ""

        print("[AudioInput] Available input devices:")
        for i in range(num_devs):
            dev = self._pyaudio_instance.get_device_info_by_host_api_device_index(0, i)
            if dev.get("maxInputChannels", 0) > 0:
                name = dev.get("name", "")
                rate = int(dev.get("defaultSampleRate", self.RATE))
                print(f"  [{i}] {name}  (rate={rate})")
                found = True

                # ✅ FIX: Realtek ya actual mic prefer karo
                # Sound Mapper / VoiceMeeter / virtual devices skip karo
                skip_keywords = ["sound mapper", "voicemeeter", "virtual", "stereo mix", "what u hear"]
                prefer_keywords = ["realtek", "microphone", "mic", "input"]

                name_lower = name.lower()
                is_skip = any(k in name_lower for k in skip_keywords)
                is_prefer = any(k in name_lower for k in prefer_keywords)

                if not is_skip and is_prefer and chosen is None:
                    chosen = i
                    chosen_name = name
                elif not is_skip and chosen is None:
                    # fallback — pehla non-virtual device
                    chosen = i
                    chosen_name = name

        # agar koi preferred nahi mila toh index 0
        if found and chosen is None:
            chosen = 0
            dev = self._pyaudio_instance.get_device_info_by_host_api_device_index(0, 0)
            chosen_name = dev.get("name", "Unknown")

        if found:
            dev = self._pyaudio_instance.get_device_info_by_host_api_device_index(0, chosen)
            self.device_index = chosen
            self.input_rate   = int(dev.get("defaultSampleRate", self.RATE))
            self.chunk_size   = int(self.input_rate * (self.CHUNK_MS / 1000.0))

            # RMS check
            rms = dev.get("defaultHighInputLatency", 0)
            print(f"[AudioInput] Selected device {chosen} ({chosen_name}) rate={self.input_rate}")

        if not found:
            print("[AudioInput] ERROR: No microphone found.")
        return found

    def _resample_to_target(self, in_data: bytes) -> bytes:
        if self.input_rate == self.RATE:
            return in_data
        audio    = np.frombuffer(in_data, dtype=np.int16).astype(np.float32)
        resampled = resample_poly(audio, self.RATE, self.input_rate)
        resampled = np.clip(resampled, -32768, 32767).astype(np.int16)
        return resampled.tobytes()

    def audio_callback(self, in_data, frame_count, time_info, status):
        self.chunk_count += 1
        self.byte_count  += len(in_data)
        if self.chunk_count <= 5 or self.chunk_count % 50 == 0:  # Log first 5 and every 50th
            print(f"[AudioInput] Chunk #{self.chunk_count}: {len(in_data)} bytes, total={self.byte_count}")
        
        if self.queue_manager is not None:
            data = self._resample_to_target(in_data)
            self.queue_manager.add_to_queue(data)
        else:
            print("[AudioInput] WARNING: queue_manager is None")
        return (None, pyaudio.paContinue)

    def start_capture(self) -> bool:
        try:
            if not self.initialize_microphone():
                return False

            self._stream = self._pyaudio_instance.open(
                format             = self.FORMAT,
                channels           = self.CHANNELS,
                rate               = self.input_rate or self.RATE,
                input              = True,
                input_device_index = self.device_index,
                frames_per_buffer  = self.chunk_size or int(self.RATE * (self.CHUNK_MS / 1000.0)),
                stream_callback    = self.audio_callback,
            )
            self._stream.start_stream()
            self.is_capturing = True
            self.chunk_count  = 0
            self.byte_count   = 0
            print("[AudioInput] ✓ Microphone capture started.")
            return True

        except OSError as e:
            msg = str(e).lower()
            if "permission" in msg:
                print("[AudioInput] ERROR: Microphone permission denied.")
            elif "busy" in msg or "device unavailable" in msg:
                print("[AudioInput] ERROR: Microphone is busy.")
            else:
                print(f"[AudioInput] ERROR: {e}")
            return False

        except Exception as e:
            print(f"[AudioInput] ERROR: {e}")
            return False

    def stop_capture(self) -> dict:
        try:
            if self._stream is not None:
                if self._stream.is_active():
                    self._stream.stop_stream()
                self._stream.close()
                self._stream = None
            if self._pyaudio_instance is not None:
                self._pyaudio_instance.terminate()
                self._pyaudio_instance = None
        except Exception as e:
            print(f"[AudioInput] Warning during stop: {e}")

        self.is_capturing = False
        stats = {"chunk_count": self.chunk_count, "byte_count": self.byte_count}
        print(f"[AudioInput] Capture stopped — {stats}")
        return stats

    def get_statistics(self) -> dict:
        return {"chunk_count": self.chunk_count, "byte_count": self.byte_count}