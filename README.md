Setup a docker container to run a pyhton script called whispering.py, ensure microphone is plugged in at all times

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
