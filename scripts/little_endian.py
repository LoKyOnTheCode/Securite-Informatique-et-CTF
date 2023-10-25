## pip install pyperclip
## Simple script, written to quickly get your little endian adress !
## python little_endian.py 08945156 copy 
## \x56\x51\x94\x08
## Copied to your clipboard ;) 
## Just paste it !!

import sys
import os

if len(sys.argv) < 2:
        print('Usage : python little_endian.py <adress_to_convert> [copy | ]')
        sys.exit(1)
else:
        chars = sys.argv[1]
        res = [chars[i:i+2] for i in range(0, len(chars), 2)][::-1]
        addr = r'\x' + r'\x'.join(res)
        print(addr)
        if len(sys.argv) > 2 and len(sys.argv) < 4:
                if sys.argv[2] == 'copy':
                        try :
                                import pyperclip
                                if os.geteuid != 0:
                                        pyperclip.copy(addr)
                                        print("Copied to your clipboard ;)")
                                else:
                                        print("If you want to copy to clipboard, do not run this script as root.")
                                        sys.exit(1)

                        except Exception as e:
                                print("Canno't import pyperclip library")
                                sys.exit(1)
                else:
                        pass
        else:
                pass
        sys.exit(0)
