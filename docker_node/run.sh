apt update && apt upgrade -y
cd /workspace/myCode/docker_node/
pip install --upgrade pip
pip install -r requirements.txt
sleep 10
apt install nodejs -y
apt install npm -y
npm init


# apt install python3-pip -y
# apt install python -y