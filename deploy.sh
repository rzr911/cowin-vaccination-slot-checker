cd cowin-vaccination-slot-checker/
pyenv activate cowin
pip install -r requirements.txt
pkill -9 -f main_cowin.py
git pull origin main
python main_cowin.py