"""
Module 1 - Initialization Module
Member 1: Eman Afzal

This module sets up all the basic variables that will be used
throughout the Offline Real-Time Speech-to-Text system.
"""

class InitializationModule:
    def __init__(self):
        # Initial system state setup

        # This flag tells the system whether microphone listening is active or not.
        # True = listening, False = idle.
        self.listening_state = False
        
        # This list will temporarily store incoming audio chunks.
        # Later, Member 4 will convert this into a proper Queue structure.
        self.audio_data_queue = []
        
        # This list will store all the final recognized sentences
        # generated during a recording session.
        self.transcription_storage = []
        
        # This variable keeps track of how long a session runs.
        # It will store the total processing time.
        self.processing_time_tracker = 0.0
        
        # This will later connect to the log file created in the Logging Module.
        # For now, it starts as None.
        self.log_file_handler = None
        
        # This string temporarily holds live partial transcription
        # while the user is speaking.
        self.partial_result_buffer = ""

    # Core Functions

    def get_all_variables(self):
        """
        Returns all important system variables in dictionary form.
        This will be used by the Session Controller (Member 9)
        to access the system state at the start.
        """
        return {
            'listening_state': self.listening_state,
            'audio_data_queue': self.audio_data_queue,
            'transcription_storage': self.transcription_storage,
            'processing_time_tracker': self.processing_time_tracker,
            'log_file_handler': self.log_file_handler,
            'partial_result_buffer': self.partial_result_buffer
        }

    def reset_for_new_session(self):
        """
        Clears previous session data so that a fresh recording
        session can start without leftover values.
        """
        self.transcription_storage = []
        self.processing_time_tracker = 0.0
        self.partial_result_buffer = ""
        self.listening_state = False

    # Helper Functions

    def set_listening_state(self, state):
        """
        Updates the listening state of the system.
        Only Boolean values (True or False) are allowed.
        """
        if isinstance(state, bool):
            self.listening_state = state
        else:
            raise ValueError("Listening state must be True or False.")

    def get_listening_state(self):
        """
        Simply returns whether the system is currently listening.
        """
        return self.listening_state

    def update_time_tracker(self, start_time, end_time):
        """
        Calculates the total time taken for a session
        and stores the difference.
        """
        if end_time >= start_time:
            self.processing_time_tracker = end_time - start_time
        else:
            raise ValueError("End time must be greater than or equal to start time.")

    def validate_initialization(self):
        """
        Checks whether all variables are properly created
        and have the correct data types.

        Returns:
            (True, message) if everything is correct
            (False, error message) if something is wrong
        """
        try:
            if not isinstance(self.listening_state, bool):
                return False, "listening_state must be Boolean."

            if not isinstance(self.audio_data_queue, list):
                return False, "audio_data_queue must be a list."

            if not isinstance(self.transcription_storage, list):
                return False, "transcription_storage must be a list."

            if not isinstance(self.processing_time_tracker, float):
                return False, "processing_time_tracker must be a float."

            if self.log_file_handler is not None and not hasattr(self.log_file_handler, "write"):
                return False, "log_file_handler must be None or a valid file handler."

            if not isinstance(self.partial_result_buffer, str):
                return False, "partial_result_buffer must be a string."

            return True, "Initialization validated successfully."

        except Exception as e:
            return False, f"Validation error: {str(e)}"

# Optional Testing Block (Runs only if file executed directly)

if __name__ == "__main__":
    init = InitializationModule()
    result = init.validate_initialization()
    print("Validation Result:", result)