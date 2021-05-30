cd cowin-vaccination-slot-checker/
docker kill redis
docker run --rm -d --name redis -p 6379:6379 -u 1007 -v /tmp:/etc redis
echo $HOME;export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv activate cowin
pip install -r requirements.txt
pkill -9 -f main.py
git pull origin main
nohup python -u main.py </dev/null >/dev/null 2>&1 &  
