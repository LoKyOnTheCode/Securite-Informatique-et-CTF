# Stabiliser un shell

```
python3 -c 'import pty;pty.spawn("/bin/bash")'
```
Ctrl + Z
```
stty raw -echo; fg
```
```
export TERM=xterm
```

Appuyer sur Entrée ou entrer une commande (exemple: ls)

