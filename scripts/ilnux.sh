#!/bin/bash
bold="\e[1m"
end="\e[0m"

blue="\e[34m"
red="\e[31m"
yellow="\e[33m"

bblue="${blue}${bold}"
byellow="${yellow}${bold}"
bred="${red}${bold}"

echo -e "\n${bold}Kernel : ${end}" && uname -s
echo -e "\n${bold}Host name : ${end}" && uname -n
echo -e "\n${bold}Kernel release : ${end}" && uname -r
echo -e "\n${bold}Kernel version : ${end}" && uname -v
echo -e "\n${bold}Hardware architecture : ${end}" && uname -i
echo -e "\n${bold}OS : ${end}" && uname -o

echo -e "\n\n===========+===========\n${bold}Checking directories...${end}\n===========+==========="
echo -e "\n${byellow}/var/www/ ${end}\n=======+=======" && ls -laR --color=auto /var/www/
echo -e "\n${byellow}/home/${end}\n=======+=======" && ls -la --color=auto /root/ 2>/dev/null || echo "You are not root :/" && ls -laR --color=auto /home/${USER} 2>/dev/null
echo -e "\n${byellow}/opt/${end}\n=======+=======" && ls -laR --color=auto /opt
echo -e "\n${byellow}/tmp/${end}\n=======+=======" && ls -laR --color=auto /tmp 2>/dev/null

echo -e "\n\n===========+===========\n${bold}Checking sudo right${end}\n===========+===========\n"
sudo -l || echo "Can't check for ${USER}"

echo -e "\n\n===========+===========\n${bold}Checking binaries w/ root perm${end}\n===========+===========\n"
find / -user root -perm -4000 -exec ls -ldb {} \; 2>/dev/null
