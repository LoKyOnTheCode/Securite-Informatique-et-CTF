# Usage de GDB 

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

#### Avancer de 1 instructions

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
