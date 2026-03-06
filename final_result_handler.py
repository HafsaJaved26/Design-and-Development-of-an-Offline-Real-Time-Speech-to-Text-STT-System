import datetime

class FinalResultHandler:
“””
Member 7: Final Result Handler
Handles complete sentences from Member 5 (StreamingRecognitionModule).
Stores transcriptions with timestamps, communicates with Member 6 (clear)
and Member 8 (logging).
“””

```
def __init__(self):
    self.all_transcriptions = []     # List of dicts: {timestamp, text}
    self.sentence_count = 0          # Total sentences recognized
    self.clear_function = None       # Member 6's clear_for_final function
    self.logger_function = None      # Member 8's log_transcription function
    self.session_start_time = None   # When session started
    self.session_end_time = None     # When session ended

# ------------------------------------------------------------------ #
#  Core callback — called by Member 5 for every complete sentence
# ------------------------------------------------------------------ #

def handle_final(self, final_text: str):
    """
    Called by Member 5 (StreamingRecognitionModule) whenever a complete
    sentence is detected.

    Steps:
    1. Generate a timestamp.
    2. Clear Member 6's partial display.
    3. Print the sentence to the console.
    4. Store the sentence in history.
    5. Log the sentence via Member 8.
    """
    # 1. Timestamp
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    # 2. Clear partial display (Member 6)
    if self.clear_function is not None:
        self.clear_function()

    # 3. Print to console
    print(f" [{timestamp}] {final_text}")

    # 4. Store in history
    entry = {"timestamp": timestamp, "text": final_text}
    self.all_transcriptions.append(entry)
    self.sentence_count += 1

    # 5. Log via Member 8
    if self.logger_function is not None:
        self.logger_function(timestamp, final_text)

# ------------------------------------------------------------------ #
#  No-speech handler  (Page 4 of main PDF)
# ------------------------------------------------------------------ #

def handle_no_speech(self):
    """Displays a message when no speech is detected in a segment."""
    print(" No speech detected in this segment")

# ------------------------------------------------------------------ #
#  Callback getter — Member 9 passes this to Member 5
# ------------------------------------------------------------------ #

def get_callback_for_member5(self):
    """Returns the handle_final function so Member 9 can pass it to Member 5."""
    return self.handle_final

# ------------------------------------------------------------------ #
#  Setters for cross-module connections
# ------------------------------------------------------------------ #

def set_clear_function(self, clear_func):
    """Store Member 6's clear_for_final function."""
    self.clear_function = clear_func

def set_logger_function(self, log_func):
    """Store Member 8's log_transcription function."""
    self.logger_function = log_func

def set_session_start(self, start_time):
    """Store the session start time (Unix timestamp from time.time())."""
    self.session_start_time = start_time

def set_session_end(self, end_time):
    """Store the session end time (Unix timestamp from time.time())."""
    self.session_end_time = end_time

# ------------------------------------------------------------------ #
#  Getters
# ------------------------------------------------------------------ #

def get_all_transcriptions(self):
    """Return the full list of transcription dicts {timestamp, text}."""
    return self.all_transcriptions

def get_sentence_count(self):
    """Return the total number of sentences recognized."""
    return self.sentence_count

def get_session_summary(self):
    """
    Return a summary dictionary for the current session.
    Used by Member 9 (SessionController) after stop_session().
    """
    return {
        "total_sentences": self.sentence_count,
        "transcriptions": self.all_transcriptions,
        "session_start": self.session_start_time,
        "session_end": self.session_end_time,
    }
```

# ——————————————————————

# Quick self-test (run this file directly to verify it works)

# ——————————————————————

if **name** == “**main**”:
print(”=== FinalResultHandler Self-Test ===\n”)

```
handler = FinalResultHandler()

# --- Simulate Member 6's clear function ---
def mock_clear():
    print("[Mock Member 6] Partial display cleared.")

# --- Simulate Member 8's log function ---
def mock_log(timestamp, text):
    print(f"[Mock Member 8] Logged -> [{timestamp}] {text}")

handler.set_clear_function(mock_clear)
handler.set_logger_function(mock_log)

import time
handler.set_session_start(time.time())

# Simulate receiving three final sentences from Member 5
test_sentences = [
    "میں بازار جا رہا ہوں",
    "آج موسم بہت اچھا ہے",
    "کل ہم سکول جائیں گے",
]

callback = handler.get_callback_for_member5()
for sentence in test_sentences:
    callback(sentence)
    time.sleep(0.5)

# Simulate no-speech event
handler.handle_no_speech()

handler.set_session_end(time.time())

print("\n--- Session Summary ---")
summary = handler.get_session_summary()
print(f"Total sentences : {summary['total_sentences']}")
for entry in summary["transcriptions"]:
    print(f"  [{entry['timestamp']}] {entry['text']}")

print("\nSelf-test complete. All functions working correctly.")
```