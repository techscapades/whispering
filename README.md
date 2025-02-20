Setup a docker container to run a pyhton script called whispering.py, ensure microphone is plugged in at all times

python script flow:
1. User input 'w' to start recording
2. user input 'q' to stop and process recording
3. user input 'ctrl + c' to quit programme

Setup on linux host system shell:
1. install docker
2. usermod -aG audio $(whoami)
3. wget -O /etc/install_whispering.sh https://raw.githubusercontent.com/techscapades/whispering/main/install_whispering.sh
4. docker run -t -d --device /dev/snd --privileged --network host --name whisper-dev -v /etc/install_whispering.sh:/install_whispering.sh ubuntu
5. docker exec -it whisper-dev /bin/bash
6. bash install_whispering.sh
7. if mic is not plugged in: plug it in, exit and reboot system
8. if mic was plugged in: run python3 whispering.py

Start app from host:
1. docker start whisper-dev && docker exec -it whisper-dev bash -c "python3 /whispering.py || exec bash"
   
OR

1. docker start whisper-dev && docker exec -it whisper-dev bash -c "python3 /whispering.py; exec bash"


