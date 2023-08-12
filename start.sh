echo "Starting interface..."
sudo FLASK_APP=interface/app.py flask run -h 0.0.0.0 -p 80 &
sleep 5
firefox http://localhost --kiosk