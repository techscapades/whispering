**Aim: Dockerise whisper.cpp and have it act as an offline speech to text "sensor" using python and user input which runs on low power hardware like the nanopi neo3**

**--> RELEASED .tar docker image with pre-downloaded tiny.en model <--**

Manual set up of a docker container to run a python script called whispering.py, ensure microphone is plugged in at all times

python script flow:
1. User input 'w' to start recording
2. user input 'q' to stop and process recording
3. user input 'ctrl + c' to quit programme

Setup on linux host system shell:
1. install docker
2. docker pull ubuntu
3. usermod -aG audio $(whoami)
4. wget -O /etc/install_whispering.sh https://raw.githubusercontent.com/techscapades/whispering/main/install_whispering.sh
5. docker run -t -d --device /dev/snd --privileged --network host --name whisper-dev -v /etc/install_whispering.sh:/install_whispering.sh ubuntu
6. docker exec -it whisper-dev /bin/bash
7. bash install_whispering.sh
8. if mic is not plugged in: plug it in, exit and reboot system
9. if mic was plugged in: run python3 whispering.py

Start app from host:
1. docker start whisper-dev && docker exec -it whisper-dev bash -c "python3 /whispering.py || exec bash"
   
OR

1. docker start whisper-dev && docker exec -it whisper-dev bash -c "python3 /whispering.py; exec bash"

Modifying whisper model for speed or accuracy ex: tiny to base model after installation:
1. download the base model by going into whisper.cpp directory using cd /whisper.cpp
2. run this command bash ./models/download-ggml-model.sh base.en
3. in the whispering.py file, modify the process_audio() function under the variable name whisper_command
4. change "/whisper.cpp/models/ggml-tiny.en.bin" to "/whisper.cpp/models/ggml-base.en.bin"
5. save and rerun whispering.py
6. avaiable models:

      tiny tiny.en tiny-q5_1 tiny.en-q5_1 tiny-q8_0
      base base.en base-q5_1 base.en-q5_1 base-q8_0
      small small.en small.en-tdrz small-q5_1 small.en-q5_1 small-q8_0
      medium medium.en medium-q5_0 medium.en-q5_0 medium-q8_0
      large-v1 large-v2 large-v2-q5_0 large-v2-q8_0 large-v3 large-v3-q5_0 large-v3-turbo large-v3-turbo-q5_0 large-v3-turbo-q8_0

7a. if you happen to have more than 1 sound device, just modify the whispering.py file and add "plughw: 3" etc...:

    def find_working_device():
     devices = ["plughw:2", "plughw:1", "plughw:0"]  # Add more if needed

7b. or you can hardcode a specific sound device by replacing this line: 

    replace: WORKING_DEVICE = find_working_device()
    to     : WORKING_DEVICE = "plughw:2"

   

On my Nanopi neo3, the difference between tiny and base is an average 2x longer inference time using base even though it is more accurate. That said as long as the audio is clear on the tiny model, there isn't as much of a difference unless short-hands for words are used, ex: mic for microphone does have better results on base than tiny

