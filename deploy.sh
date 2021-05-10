cd cowin-vaccination-slot-checker/
docker-compose down
docker-compose up -d
echo $HOME;export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv activate cowin
pip install -r requirements.txt
pkill -9 -f main.py
git pull origin main
nohup python -u main.py </dev/null >/dev/null 2>&1 &  
