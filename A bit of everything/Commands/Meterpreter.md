# Meterpreter

Quelques commandes utiles

## URLs

https://infinitelogins.com/2020/01/25/msfvenom-reverse-shell-payload-cheatsheet/


## Shell 2 meterpreter
```
search shell_to_meterpreter
use 0
```
Ensuite on choisi la session que l'on souhaite faire évoluée

```
sessions
set session X
```
Où "X" est le numéro de session. Ensuite on `run`.

## Hashdump

```
search hashdump
```
