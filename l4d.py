from pathlib import Path
import  os, shutil
from datetime import datetime
import shutil
from itertools import chain
import zipfile
import patoolib


"""
Small script to move all non test maps into non testing folder and unzip any rar/zip files and move the maps into the addon folder
Excludes moving/removing specified files 
"""

downloadspath = Path(Path.home() / 'Downloads')
today = datetime.today()

addonsdir = Path(r'C:\Program Files (x86)\Steam\steamapps\common\left 4 dead\left4dead\addons')
nontestmapsdir = addonsdir / 'move maps here'

filesinaddonsfolder = [file for file in addonsdir.iterdir() if file.suffix == '.vpk']
filesToIgnore = [
    'l4dautoconfig.vpk',
    'readme.txt',
    'removedmainlobbymusic.vpk',
    'silencemod.vpk',
    'team health counter.vpk',
    'viewmodeloverride.dll',
    'viewmodeloverride.vdf'
]

for file in addonsdir.iterdir():
    if file.name in filesToIgnore:
        continue


if len(filesinaddonsfolder) > 50:
    print('enabling testing mode')
    if not nontestmapsdir.exists():
        Path.mkdir(nontestmapsdir)

    for file in addonsdir.iterdir():
        if file.name in filesToIgnore:
            continue
        if file.suffix == '.vpk':
            try:
                shutil.move(file, nontestmapsdir)
            except Exception as error:
                print(f'FAILED TO MOVE FILE: [{error}]')

    for file in chain(downloadspath.glob('*.zip'), downloadspath.glob('*.rar')):
        date = datetime.fromtimestamp(int(float(file.stat().st_birthtime)))
        if date.date() == today.date():
            print(file)
            if file.suffix == '.zip':
                with zipfile.ZipFile(file, 'r') as zip_ref:
                    zip_ref.extractall(addonsdir)
                    
            if file.suffix == '.rar':
                patoolib.extract_archive(str(file), outdir=addonsdir)
        

else:
    print('disabling testing mode')
    for file in addonsdir.iterdir():
        if file.name in filesToIgnore:
            continue

        if file.is_dir():
            continue
        
        print(f'Deleting file: [{file.name}]')
        os.remove(file)        

            

    for file in nontestmapsdir.iterdir():
        if file.name in filesToIgnore:
            continue

        if file.suffix == '.vpk':
            try:
                shutil.move(file, addonsdir)
            except Exception as error:
                print(f'FAILED TO MOVE FILE: [{error}]')




