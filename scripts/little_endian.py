import sys
import os

if len(sys.argv) < 2:
        print('Usage : python little.py <adress_to_convert> [copy | ]')
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
