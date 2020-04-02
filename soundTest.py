import os
import platform
syst = platform.system()
if syst == 'Linux':
    os.system('spd-say "your program has finished"')
elif syst == 'Darwin':
    os.system('say "your program has finished"')
