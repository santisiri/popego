from __future__ import with_statement
import os
import sys
import re

codingLine = re.compile("coding[:=]\s*([-\w.]+)")
docformatLine = re.compile("^__docformat__")

basePath = sys.argv[1] if len(sys.argv) > 1 else '.'

pyFiles = []
for base, dirs, files in os.walk(basePath):
    currentPyFiles = filter(lambda s:s.endswith('.py'), files)
    pyFiles.extend([base+'/'+f for f in currentPyFiles])

for fname in pyFiles:
    with open(fname,'r+') as f:
        lines = f.readlines()
        f.seek(0)
        
        if len(lines) == 0 or not codingLine.search(lines[0]):
            lines.insert(0,"# -*- coding: utf-8 -*-\n")
        if len(lines) == 1 or not docformatLine.search(lines[1]):
            lines.insert(1,"__docformat__='restructuredtext'\n")
        
        f.writelines(lines)
