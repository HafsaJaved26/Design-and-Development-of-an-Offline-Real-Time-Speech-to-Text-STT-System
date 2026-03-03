Initialization Module – Variable Documentation
1️⃣ listening_state (Boolean)

Purpose: Indicates whether the system is actively listening.
True → Microphone streaming active
False → System idle

2️⃣ audio_data_queue (List)

Temporary storage for incoming audio chunks.
Later converted into a proper Queue by Audio Queue Module.
Used for streaming architecture (Producer → Consumer pattern).

3️⃣ transcription_storage (List)

Stores all final recognized sentences during a session.
Used by Final Result Handler and Logging Module.

4️⃣ processing_time_tracker (Float)

Stores total duration of a recording session.
Calculated when session ends.

5️⃣ log_file_handler (File Object / None)

Placeholder for log file connection.
Connected later by Logging Module.

6️⃣ partial_result_buffer (String)

Stores temporary live transcription text.
Updated continuously during streaming recognition.
Cleared when final sentence is detected.