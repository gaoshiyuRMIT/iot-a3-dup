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
