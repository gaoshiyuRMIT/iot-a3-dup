import hashlib
password = 'duan953280'
h = hashlib.md5(password.encode())
print(h.hexdigest())

from configparser import ConfigParser

config = ConfigParser()
config.read('ap.config', encoding='UTF-8')

print(config['address'].getint('port'))
print(config['address'].get('apiAdd'))


# {
#     "username": "xinhuanduan",
#     "password": "a6096d7f16360d8ce5e81dfa947972f6",
#     "fName": "Xinhuan",
#     "lName": "Duan",
#     "email": "duanxinhuan@163.com"
# }


