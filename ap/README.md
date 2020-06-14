### Usage 
- cd into the ap folder
- change the port and ip to the osame port and ip of your server in ap.config
- `python engmain.py`
- `workon barcode`



### Prerequisites under console
- `sudo apt-get install bluetooth`
- `sudo apt-get install python-bluez`
- `sudo apt-get install bluez`
- `sudo apt-get install bluetooth bluez libbluetooth-dev`
- `pip install opencv-python == 3.4.6.27`
- `sudo apt-get install libzbar0`


### Prerequisites under virtual environment
- `mkvirtualenv barcode -p python3`
- `workon barcode`
- `pip install qrcode[pil]`
- `pip install pyzbar`
- `pip install matplotlib`


