# -*- coding: utf-8 -*-
import os, sys, shutils

if len(sys.argv) <= 1:
    print('debe llamar al sistema usando : ')
    print('python3 ' + sys.argv[0] + ' usuario dni')
    exit(1)

usuario = sys.argv[1]
dni = sys.argv[2]

os.chdir('/home')
os.rename(usuario,dni)
os.chdir('/home/samba/profiles')
os.rename(usuario,dni)

"""

    -- cambiar los permisos al directorio --
    /home/dni
    /home/samba/profiles/dni

"""

for ruta, dirs, archivos in os.walk('/home/' + dni):
    shutil.chown(ruta, dni, 'root')
    for archivo in archivos:
        shutil.chown(archivo, dni, 'root')

for ruta, dirs, archivos in os.walk('/home/samba/profiles/' + dni):
    shutil.chown(ruta, dni, 'root')
    for archivo in archivos:
        shutil.chown(archivo, dni, 'root')
