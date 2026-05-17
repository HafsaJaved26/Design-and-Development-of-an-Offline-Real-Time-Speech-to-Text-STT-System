# -*- coding: utf-8 -*-
"""
audio_queue_manager_module.py
Member 4 (Afia Noor) — Audio Queue Manager Module
Thread-safe FIFO buffer between AudioInputModule and StreamingRecognitionModule.
"""

import queue


class AudioQueueManagerModule:
    """
    Thread-safe queue that decouples audio capture (producer)
    from speech recognition (consumer).
    """

    def __init__(self, max_size: int = 200):
        self.max_size         = max_size
        self.audio_queue      = queue.Queue(maxsize=max_size)

        # Statistics counters
        self.total_received   = 0   # chunks successfully enqueued
        self.total_sent       = 0   # chunks successfully dequeued
        self.queue_full_count = 0   # times add was attempted on a full queue
        self.queue_empty_count= 0   # times get was attempted on an empty queue
        self.dropped_chunks   = 0   # chunks discarded because queue was full

    # ── Producer side (called by AudioInputModule) ────────────────────────────

    def add_to_queue(self, audio_chunk: bytes) -> bool:
        """
        Attempt to enqueue an audio chunk without blocking.
        Returns True on success, False if the queue is full (chunk dropped).
        """
        try:
            self.audio_queue.put_nowait(audio_chunk)
            self.total_received += 1
            return True
        except queue.Full:
            self.queue_full_count += 1
            self.dropped_chunks   += 1
            print(f"[Queue] FULL - chunk dropped, total dropped: {self.dropped_chunks}")
            return False

    # ── Consumer side (called by StreamingRecognitionModule) ──────────────────

    def get_from_queue(self):
        """
        Attempt to dequeue an audio chunk without blocking.
        Returns the chunk on success, None if the queue is empty.
        """
        try:
            chunk = self.audio_queue.get_nowait()
            self.total_sent += 1
            return chunk
        except queue.Empty:
            self.queue_empty_count += 1
            return None

    # ── Inspection ────────────────────────────────────────────────────────────

    def get_queue_size(self) -> int:
        """Return the current number of items waiting in the queue."""
        return self.audio_queue.qsize()

    def is_queue_full(self) -> bool:
        """Return True if the queue has reached its maximum capacity."""
        return self.audio_queue.qsize() >= self.max_size

    def is_queue_empty(self) -> bool:
        """Return True if the queue contains no items."""
        return self.audio_queue.empty()

    def get_statistics(self) -> dict:
        """Return a full statistics snapshot."""
        current = self.audio_queue.qsize()
        return {
            "total_received":    self.total_received,
            "total_sent":        self.total_sent,
            "queue_full_count":  self.queue_full_count,
            "queue_empty_count": self.queue_empty_count,
            "dropped_chunks":    self.dropped_chunks,
            "current_size":      current,
            "max_size":          self.max_size,
            "utilization_percentage": round(current / self.max_size * 100, 1),
        }

    def clear_queue(self):
        """
        Discard all items currently in the queue and reset all counters.
        Used when starting a fresh session.
        """
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                break

        self.total_received    = 0
        self.total_sent        = 0
        self.queue_full_count  = 0
        self.queue_empty_count = 0
        self.dropped_chunks    = 0
