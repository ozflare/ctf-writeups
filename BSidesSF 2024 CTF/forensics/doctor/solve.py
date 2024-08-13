#!/usr/bin/env python3
import zipfile

archive = zipfile.ZipFile('SuperSecretWordDoc.docx')

for file in archive.filelist:
    if file.filename == 'word/media/image0.png':
        archive.extract(file)
        break
