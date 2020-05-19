import hashlib
password = 'duan953280'
h = hashlib.md5(password.encode())
print(h.hexdigest())


# {
#     "username": "xinhuanduan",
#     "password": "a6096d7f16360d8ce5e81dfa947972f6",
#     "fName": "Xinhuan",
#     "lName": "Duan",
#     "email": "duanxinhuan@163.com"
# }