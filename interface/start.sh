echo "Starting interface..."
sudo flask run -h 0.0.0.0 -p 80 --debug &
firefox --kiosk http://localhost &
exit 0