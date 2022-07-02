#!/usr/bin/env python
from pathlib import Path
import subprocess

baseDir = Path.cwd()
for fn in baseDir.rglob('*.wav') :
    newfn = fn.with_suffix('.flac')
    extCmd = ['ffmpeg', '-i', str(fn), str(newfn)]
    pout2 = subprocess.run(extCmd, capture_output=True)
    if pout2.returncode == 0 :
        fn.unlink()
    else :
        print(str(fn))
    

    #print(s)
