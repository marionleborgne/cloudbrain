pyinstaller --onefile -y --clean ../main.py
rm -rf build
rm main.spec
rm -rf osx
mv dist osx
