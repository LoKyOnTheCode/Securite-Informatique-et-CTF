# Usage de GDB 

<br>
<br>

[Infos sur les fonctions](#Infos-sur-les-fonctions)
[Mettre un breakpoint sur une adresse](#Mettre-un-breakpoint-sur-une-adresse)
[Tester le programme](#Tester-le-programme)
[Avancer de 1 instruction](#Avancer-de-1-instruction)
[Les registres](#Les-registres)
  [Avoir des infos](#Avoir-des-infos)
  [Lire le contenu d'une adresse ou un registre](#Lire-le-contenu-d'une-adresse-ou-un-registre)
[Executer jusqu'au prochain breakpoint](#Executer-jusqu'au-prochain-breakpoint)
  
<br>
<br>

GEF (surcouche de GDB) : 

```
https://github.com/hugsy/gef
```

#### Infos sur les fonctions

```
i functions
```

#### Mettre un breakpoint sur une adresse

```
b *<address>
```

#### Tester le programme

```
run <argument>
```

#### Avancer de 1 instruction

```
step
```

#### Les registres

##### Avoir des infos

```
i registers
```
ou 
```
i r
```

##### Lire le contenu d'une adresse ou un registre

```
x/s <argument>
```

#### Executer jusqu'au prochain breakpoint

```
continue
```

ou
```
c
```
