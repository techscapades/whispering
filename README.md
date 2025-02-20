Setup a docker container to run a pyhton script called whispering.py

python script flow:
1. User input 'w' to start recording
2. user input 'q' to stop and process recording
3. user input 'ctrl + c' to quit programme

Setup on linux host system shell:
1. install docker
2. usermod -aG audio $(whoami)
3. 
4. docker run -t -d --device /dev/snd --privileged --network host --name whisper-dev ubuntu
5. docker exec -it whisper-dev /bin/bash
