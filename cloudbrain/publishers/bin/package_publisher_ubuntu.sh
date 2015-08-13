pyinstaller --onefile -y --clean ../sensor_publisher.py
rm -rf build
rm sensor_publisher.spec
rm -rf ubuntu
mv dist ubuntu
