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

echo -e "\n\n===========+===========\n${bold}Checking binaries w/ root perm${end}\n===========+===========\n"
find / -user root -perm -4000 -exec ls -ldb {} \; 2>/dev/null
