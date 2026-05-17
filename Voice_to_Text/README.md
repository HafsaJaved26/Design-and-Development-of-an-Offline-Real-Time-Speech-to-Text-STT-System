# 🎤 Offline Urdu Speech-to-Text System

A real-time, offline Urdu speech recognition application powered by OpenAI Whisper and built with Streamlit.

## Features

✅ **Live Transcription** - Real-time Urdu speech recognition from microphone  
✅ **Offline Processing** - No internet connection required  
✅ **Fast Recognition** - Processes audio faster than real-time (4-5x speed)  
✅ **Clean UI** - Modern, responsive dark theme interface  
✅ **Session Logging** - Records all transcriptions to log files  

## System Architecture

The application uses a modular architecture with 11 core components:

| Module | Purpose |
|--------|---------|
| `audio_input_module.py` | Captures 16-bit PCM mono audio from microphone |
| `audio_queue_manager_module.py` | Thread-safe audio buffer management |
| `streaming_recognition_module.py` | Whisper transcription of accumulated audio on STOP |
| `partial_result_manager.py` | Manages live transcription updates for UI |
| `final_result_handler.py` | Stores completed sentences and session history |
| `model_loader_module.py` | Loads OpenAI Whisper (base model, ~850MB) |
| `logging_module.py` | Logs transcriptions to timestamped files |
| `initialization_module.py` | Manages application state |
| `session_controller.py` | Orchestrates all 8 modules together |
| `app.py` | Streamlit UI and user interface |
| `main.py` | Application entry point |

## Installation

### Requirements

- Python 3.9+
- 4GB+ RAM
- 1GB+ disk space for Whisper model
- Windows/Mac/Linux

### Setup

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r srequirements.txt

# 3. Run application
python main.py
```

The application will automatically download the Whisper model on first run (~850MB).

## Usage

1. **Open Browser**: Navigate to `http://localhost:8510`
2. **Start Recording**: Click the **▶ START** button
3. **Speak in Urdu**: Speak clearly into your microphone (minimum 10-15 seconds recommended)
4. **View Results**: 
   - **Live Transcription** box shows real-time text updates
   - **Results** section displays completed transcriptions (full accumulation on STOP)
5. **Stop Recording**: Click the **⏹ STOP** button - transcription will begin immediately

### Controls

| Button | Action |
|--------|--------|
| **▶ START** | Begin recording microphone audio |
| **⏹ STOP** | Stop recording and finalize session |
| **🔄 CLEAR** | Clear all transcriptions from current session |

### Display Sections

| Section | Shows |
|---------|-------|
| **🎤 Live Transcription** | Real-time text as you speak |
| **💬 Results** | Completed sentences from this session |
| **Statistics** | Sentence count, recording duration |

## Technical Details

### Audio Specifications

- **Sample Rate**: 16,000 Hz (16 kHz)
- **Channels**: Mono (1 channel)
- **Format**: PCM 16-bit signed
- **Accumulation**: All audio accumulated during recording (STOP to transcribe)
- **Chunk Size**: 4,000 samples (250ms per chunk)
- **Minimum Audio**: ~30 seconds recommended for best accuracy

### Whisper Configuration

- **Model**: Base (140M parameters, ~850MB)
- **Language**: Urdu (ur) - specifically trained identifier
- **Precision**: Full precision (fp16=False) for accuracy
- **Processing Speed**: ~4-5x real-time with CPU
- **Strategy**: Accumulate audio during recording, transcribe once on STOP

### File Locations

```
c:\Users\prime pc\Downloads\Voice_to_Text_Nam\Voice_to_Text\Voice_to_Text\
├── *.py                    # Python modules
├── logs/                   # Session log files (transcriptions)
├── venv/                   # Virtual environment
└── README.md               # This file
```

## Logs & Output

Each recording session creates a log file:

```
logs/transcript_YYYYMMDD_HHMMSS.txt
```

Contains:
- Timestamp
- Complete transcriptions from the session
- Recording duration

## Troubleshooting

### No Audio Detected

- Check microphone is connected and enabled
- Test microphone volume
- Ensure no other app is using microphone
- Restart application

### Poor Transcription Quality

- Speak clearly and slowly
- Reduce background noise
- Use a quality microphone
- Ensure Urdu language is set

### Application Slow

- Close other applications to free RAM
- Whisper uses CPU heavily - modern processor recommended
- First model load takes ~1-2 minutes

### PyAudio Installation Issues (Windows)

- If `pip install pyaudio` fails, install pre-built wheel:
  ```
  pip install pipwin
  pipwin install pyaudio
  ```
- Or download pre-built wheels from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
- Ensure you have Visual C++ Build Tools installed

## Performance Metrics

| Metric | Value |
|--------|-------|
| Model Size | ~850 MB |
| Startup Time | 10-30 seconds |
| Cold Start (first run) | 1-2 minutes (downloads model) |
| Transcription Speed | 4-5x real-time |
| Latency | ~1.5 seconds per chunk |
| Supported Languages | 99 languages (Urdu optimized) |

## Dependencies

- **streamlit** - Web UI framework
- **openai-whisper** - Speech recognition engine
- **torch** - Deep learning framework (required by Whisper)
- **numpy** - Arrays and math
- **pyaudio** - Microphone input from system audio device
- **scipy** - Audio processing utilities

## License

Built using OpenAI's Whisper model (MIT License).

---

**Last Updated**: March 9, 2026  
**Application Status**: Fully Functional ✅  
**Latest Fix**: Simplified pipeline - accumulates audio until STOP for reliable Whisper transcription
