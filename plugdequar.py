#!/usr/bin/env python
from pathlib import Path
import subprocess
import xattr

QUARANTINE_KEY = 'com.apple.quarantine'



baseDir = Path('/Library/Audio/Plug-Ins')

#for f in [i for i in baseDir.iterdir() if i.is_file()] :
#    print(f)

for d in [i for i in baseDir.rglob('*.vst') if i.is_dir()]:
    xa = xattr.xattr(d)
    if QUARANTINE_KEY in xa.keys():
        del xa[QUARANTINE_KEY]
        print(d)



# print(baseDir)
# print(dir(baseDir))

# baseDir = Path.cwd()
# for fn in baseDir.rglob('*.wav') :
#     newfn = fn.with_suffix('.flac')
#     extCmd = ['ffmpeg', '-i', str(fn), str(newfn)]
#     pout2 = subprocess.run(extCmd, capture_output=True)
#     if pout2.returncode == 0 :
#         fn.unlink()
#     else :
#         print(str(fn))
    

    #print(s)
