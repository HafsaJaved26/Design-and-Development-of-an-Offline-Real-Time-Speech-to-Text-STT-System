# -*- coding: utf-8 -*-
"""
main.py
Member 9 (M. Zaheer) — Application Entry Point
Validates all dependencies, checks the Whisper model availability,
and launches the Streamlit interface.

Usage:
    python main.py
"""

import sys
import os
import subprocess
import importlib

# Fix Unicode encoding for Windows terminal
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


# ═════════════════════════════════════════════════════════════════════════════
# ASCII banner
# ═════════════════════════════════════════════════════════════════════════════

BANNER = """
╔══════════════════════════════════════════════════════════════════╗
║        Offline Real-Time Urdu Speech-to-Text System             ║
║        Powered by OpenAI Whisper  ·  Interface by Streamlit      ║
║        Team Project — Member 9 Integration                      ║
╚══════════════════════════════════════════════════════════════════╝
"""

# ═════════════════════════════════════════════════════════════════════════════
# Required Python packages
# import_name → pip install name
# ═════════════════════════════════════════════════════════════════════════════

REQUIRED_PACKAGES = {
    "streamlit": "streamlit",
    "whisper":   "openai-whisper",
    "pyaudio":   "pyaudio",
    "numpy":     "numpy",
}

OPTIONAL_PACKAGES = {
    "streamlit_autorefresh": "streamlit-autorefresh",
    "librosa":   "librosa",  # For audio file processing
}


# ═════════════════════════════════════════════════════════════════════════════
# Helpers
# ═════════════════════════════════════════════════════════════════════════════

def check_import(module_name: str) -> bool:
    """Return True if the module can be imported, False otherwise."""
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False


def print_banner():
    print(BANNER)


def check_dependencies() -> bool:
    """
    Verify all required packages are installed.
    Prints a clear install guide if any are missing.
    Returns True if all present, False otherwise.
    """
    missing_required = {
        mod: pip
        for mod, pip in REQUIRED_PACKAGES.items()
        if not check_import(mod)
    }

    missing_optional = {
        mod: pip
        for mod, pip in OPTIONAL_PACKAGES.items()
        if not check_import(mod)
    }

    if missing_optional:
        print("  ⚠  Optional packages not found (live auto-refresh will use fallback):")
        for mod, pip in missing_optional.items():
            print(f"      pip install {pip}")
        print()

    if not missing_required:
        print("  ✓  All required dependencies are installed.")
        return True

    # Print install guide
    print("  ✗  MISSING REQUIRED PACKAGES — install before running:\n")
    for mod, pip_name in missing_required.items():
        print(f"      pip install {pip_name}")

    if "pyaudio" in missing_required:
        print()
        print("  PyAudio note:")
        print("  On Windows, if  pip install pyaudio  fails, try:")
        print("      pip install pipwin")
        print("      pipwin install pyaudio")
        print()
        print("  On Linux:")
        print("      sudo apt-get install python3-pyaudio  (Debian/Ubuntu)")
        print("      sudo dnf install python3-pyaudio      (Fedora)")
        print()
        print("  On macOS:")
        print("      brew install portaudio")
        print("      pip install pyaudio")

    print()
    return False


def check_model() -> bool:
    """
    Verify Whisper library is available.
    Whisper downloads models automatically on first use.
    Returns True if whisper can be imported.
    """
    if check_import("whisper"):
        print(f"  ✓  Whisper library found (models auto-download on first use)")
        return True

    print(f"  ✗  Whisper library not found")
    print("  Install with:  pip install openai-whisper")
    print()
    return False


def check_app_file() -> str:
    """Return the absolute path to app.py, or empty string if not found."""
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
    if os.path.isfile(app_path):
        print(f"  ✓  app.py found at  {app_path}")
        return app_path

    print(f"  ✗  app.py not found at  {app_path}")
    return ""


def check_ffmpeg() -> bool:
    """
    Check if FFmpeg is available (required for audio file uploads).
    Returns True if FFmpeg is found, False otherwise.
    """
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"  ✓  FFmpeg found (audio upload support enabled)")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    print(f"  ⚠  FFmpeg not found (audio file upload will be limited)")
    print("  Install FFmpeg for full audio upload functionality:")
    if sys.platform == "win32":
        print("      Download from https://ffmpeg.org/download.html")
        print("      Or use: choco install ffmpeg  (if Chocolatey installed)")
    elif sys.platform == "darwin":
        print("      brew install ffmpeg")
    else:
        print("      sudo apt-get install ffmpeg  (Debian/Ubuntu)")
        print("      sudo dnf install ffmpeg      (Fedora)")
    print()
    return False


def launch_streamlit(app_path: str):
    """
    Launch the Streamlit server.
    Blocks until the user presses Ctrl+C.
    """
    print()
    print("─" * 66)
    print("  Launching Streamlit — open your browser at:")
    print("  http://localhost:8501")
    print()
    print("  Press Ctrl+C to stop the server.")
    print("─" * 66)
    print()

    try:
        subprocess.run(
            [
                sys.executable, "-m", "streamlit", "run", app_path,
                "--server.port",      "8501",
                "--server.headless",  "false",
                "--browser.gatherUsageStats", "false",
            ],
            check=True,
        )
    except KeyboardInterrupt:
        print("\n  Server stopped by user.")
    except subprocess.CalledProcessError as exc:
        print(f"\n  ✗  Streamlit exited with error code {exc.returncode}")
        sys.exit(1)


# ═════════════════════════════════════════════════════════════════════════════
# Main
# ═════════════════════════════════════════════════════════════════════════════

def main():
    print_banner()

    print("  Checking dependencies…\n")
    deps_ok  = check_dependencies()
    model_ok = check_model()
    ffmpeg_ok = check_ffmpeg()
    app_path = check_app_file()

    print()

    if not deps_ok:
        print("  Install the missing packages above, then re-run:  python main.py")
        sys.exit(1)

    if not model_ok:
        # Non-fatal — Whisper will download the model on first use
        print("  WARNING: Whisper library not installed.")
        print("  The app will start but speech recognition will fail.")
        print()

    if not app_path:
        print("  ✗  Cannot start — app.py is missing from this directory.")
        sys.exit(1)

    launch_streamlit(app_path)


if __name__ == "__main__":
    main()
