#!/bin/bash

# Exit immediately if a command fails
set -e  

echo "🚀 Updating system packages..."
apt-get update && apt-get upgrade -y && apt autoremove -y

echo "📦 Installing dependencies..."
DEBIAN_FRONTEND=noninteractive apt install -y \
    python3 python3-pip alsa-utils cmake libsdl2-dev git htop nano curl wget \
    build-essential ccache usbutils libusb-1.0-0 ffmpeg 

echo "🌍 Downloading whispering.py..."
wget -q https://raw.githubusercontent.com/techscapades/whispering/main/whispering.py
chmod +x whispering.py

echo "🔄 Cloning whisper.cpp repository..."
git clone --depth=1 https://github.com/ggerganov/whisper.cpp.git

cd whisper.cpp

echo "📥 Downloading the tiny.en model..."
bash ./models/download-ggml-model.sh tiny.en

echo "⚙️ Building whisper.cpp..."
cmake -B build -DWHISPER_SDL2=ON
cmake --build build --config Release

echo "✅ Installation complete!"
cd /
echo "run: python3 whispering.py to start whispering :)"

