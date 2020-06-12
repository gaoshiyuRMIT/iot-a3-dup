### Usage 
- cd into the ap folder
- change the port and ip to the osame port and ip of your server in ap.config
- `python main.py`

### Prerequisites on Mac OS
- `brew install cmake`
- `brew install dlib`
- `sudo python3 -m pip install dlib`
- `inside ap, python3 -m venv --system-site-packages venv`

### Prerequisites on Raspberry Pi
- `python3 -m pip install opencv-contrib-python==4.1.0.25`
- `sudo apt-get install libatlas-base-dev`
- `sudo apt-get install libhdf5-serial-dev`
- inside ap, `python3 -m venv --system-site-packages venv`

### Bluetooth Prerequisites
- 'sudo apt-get install bluetooth'
- 'sudo apt-get install python-bluez'
- 'sudo apt-get install bluez'
- 'sudo apt-get install bluetooth bluez libbluetooth-dev'

### Prerequisites
- 'sudo apt-get install libzbar0'
- 'mkvirtualenv barcode -p python3'
- 'workon barcode'
- 'pip install qrcode[pil]'
- 'pip install pyzbar(install under virtual environment!)'
- 'pip install matplotlib'
- 'pip install opencv-python'
- 'vim.tiny .bashrc'
Add this line to the file opened by the vim.tiny
- 'export LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so'.1
- 'source .bashrc'
- 'pip install pybluez''
