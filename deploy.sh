cd cowin-vaccination-slot-checker/
sudo docker-compose down
sudo docker-compose up -d
echo $HOME;export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv activate cowin
pip install -r requirements.txt
pkill -9 -f main_cowin.py
git pull origin main
nohup python -u main_cowin.py </dev/null >/dev/null 2>&1 &  
