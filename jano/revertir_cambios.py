# -*- coding: utf-8 -*-

import csv
import os

# asigno la ruta donde estan los archivos a la variable path_profiles
path_home = '/media/jano/Archivos/python/python/jano/home/'
path_profiles = '/media/jano/Archivos/python/python/jano/home/samba/profiles/'


# abrimos el archivo csv con permisos de lectura
reader = csv.reader(open('usuarios.csv', 'rb'))
# hago un for para recorrer las filas del archivo csv
for i,row in enumerate(reader):
    # la variable mail es la columna (2) mail
    mail =  row[1]
    # usuario es la columna mail menos los 18 caracteres del dominio
    usuario = mail[0:-18]
    # la variable dni es la columna (1) dni
    dni = row[0]

    profile = path_profiles + usuario
    home = path_home + usuario
    profile_dni = path_profiles + dni
    home_dni = path_home + dni
    # reviso si existe el home del usuario en el path_home
    if os.path.isdir(home_dni):
        if os.path.islink(home):
            del home
        os.rename(home_dni, home)

    if os.path.isdir(profile_dni):
        if os.path.islink(profile):
            del profile
        os.rename(profile_dni, profile)


print bcolors.BOLD, 'Cambios realizados ', home_mod, bcolors.ENDC
