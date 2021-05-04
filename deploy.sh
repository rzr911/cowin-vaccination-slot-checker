cd cowin-vaccination-slot-checker/
echo $HOME;export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv activate cowin
pip install -r requirements.txt
pkill -9 -f main_cowin.py
git pull origin main
python main_cowin.py &