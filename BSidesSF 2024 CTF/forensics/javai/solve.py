#!/usr/bin/env python3
import zipfile

archive = zipfile.ZipFile('JavAI.docx')

for file in archive.filelist:
    if file.filename == 'getflag.class':
        archive.extract(file)
        break
