from passlib.hash import sha256_crypt

pwHash = sha256_crypt.using(rounds=1000).hash('root')
print(pwHash)
