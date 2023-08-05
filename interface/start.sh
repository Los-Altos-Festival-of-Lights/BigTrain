echo "Starting interface..."
nohup flask run -h 0.0.0.0 -p 80 --debug &
nohup firefox --kiosk http://localhost &
exit 0