# Authentication Relay 

Responder on GitHub <a href="https://github.com/lgandx/Responder">here</a>

```
sudo responder -I tun0
```

If responder cannot listen to port 389, it is probably because of SLAPD server is running. Check the current state of this port by using :
```
netstat -nat
```

Listening for events :

![image](https://user-images.githubusercontent.com/97956863/231966809-0f5612a1-11a8-4451-9be6-809306e853ed.png)

