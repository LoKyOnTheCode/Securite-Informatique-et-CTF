## Binwalk (data extraction)

```
binwalk <image> -e
```
<br>

## Hydra
### WEB
```
hydra -l <username> -P <wordlist> 10.10.0.156 http-post-form "/:username=^USER^&password=^PASS^:F=incorrect" -V
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

## 7z Deziper avec password

```
7z e file.zip
```
