su - sree
cd cowin-vaccination-slot-checker/
pkill -9 -f main_cowin.py
git pull origin main
python main_cowin.py