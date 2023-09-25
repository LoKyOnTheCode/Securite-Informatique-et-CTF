# Tools

[crackpkcs12](#crackpkcs12)


## crackpkcs12

Crackpkcs12 est un outil qui permet de cracker des certificat protégé par mots de passe.
<br>
<br>
Exemple d'utilisation:

```
crackpkcs12 -d /usr/share/wordlists/rockyou.txt cert.pfx
```

URL:
```
https://sourceforge.net/projects/crackpkcs12/files/
```
Installation:
```
tar -xf crackpkcs12*
cd crackpkcs12*
./configure
make
sudo make install
```
