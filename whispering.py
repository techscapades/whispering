import subprocess
import threading
import sys
import signal
import re

# Function to check which audio device is available
def find_working_device():
    devices = ["plughw:0", "plughw:1"]  # Add more if needed

    for device in devices:
        command = [
            "arecord", "-D", device, "-c1", "-r", "48000", "-f", "S32_LE",
            "-t", "wav", "-V", "mono", "-v", "-d", "1", "/dev/null"  # Discard recorded data
        ]
        result = subprocess.run(command, capture_output=True, text=True)

        if "audio open error" not in result.stderr:
            print(f"✅ Found working audio device: {device}")
            return device  # Return the first working device
    
    print("❌ No working audio device found. Exiting.")
    sys.exit(1)  # Exit if no device is available

# Get a working device at startup
WORKING_DEVICE = find_working_device()

# Function to run the arecord command in a subprocess
def record_audio():
    command = [
        "arecord",
        "-D", WORKING_DEVICE,  # Use the detected working device
        "-c1",
        "-r", "48000",
        "-f", "S32_LE",
        "-t", "wav",
        "-V", "mono",
        "-v", "/whisper.cpp/samples/file.wav"
    ]
    
    # Run the command as a subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for the process to complete (it will run until stopped)
    process.communicate()

# Function to wait for user input to start and stop the recording
def wait_for_user_input():
    while True:
        user_input = input("Press 'w' to start recording, 'q' to process current/previous recording or Ctrl+C to exit: ")
        if user_input.lower() == "w":
            print("🎙️ Starting the recording...")
            recording_thread = threading.Thread(target=record_audio)
            recording_thread.start()
        elif user_input.lower() == "q":
            print("🛑 Stopped and processing the recording...")
            subprocess.run(["pkill", "-f", "arecord"])  # Stop `arecord`
            break

# Function to process the recorded audio
def process_audio():
    ffmpeg_command = [
        "ffmpeg", 
        "-i", "/whisper.cpp/samples/file.wav", 
        "-ar", "16000", 
        "-ac", "1", 
        "-c:a", "pcm_s16le", 
        "/whisper.cpp/samples/output.wav", 
        "-y"
    ]
    
    # Run ffmpeg command silently
    subprocess.run(ffmpeg_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Run whisper-cli command
    whisper_command = [
        "./whisper.cpp/build/bin/whisper-cli", 
        "-m", "/whisper.cpp/models/ggml-tiny.en.bin", 
        "-f", "/whisper.cpp/samples/output.wav"
    ]
    
    # Capture output of whisper-cli
    result = subprocess.run(whisper_command, capture_output=True, text=True)
    
    # Extract transcriptions using regex
    transcription_pattern = r'\[\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\] (.+)'
    transcriptions = re.findall(transcription_pattern, result.stdout)
    
    # Print transcriptions
    print("\nTranscription Output:\n")
    for transcription in transcriptions:
        print(transcription)
    print()

# Signal handler for Ctrl+C
def signal_handler(sig, frame):
    print("\n🚪 Exiting the program...")
    sys.exit(0)

# Main function
def main():
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        wait_for_user_input()
        process_audio()

if __name__ == "__main__":
    main()

