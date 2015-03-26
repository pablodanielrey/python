# -*- coding: utf-8 -*-
import csv
import pwd
import grp
import os
# asigno la ruta donde estan los archivos a la variable path_profiles
path_profiles = '/media/jano/Archivos/Soporte/github/python/jano/home/samba/profiles/'
path_home = '/media/jano/Archivos/Soporte/github/python/jano/home/'
profiles_mod = 0
home_mod = 0

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

    # reviso si existe el profile del usuario en el path_profiles
    if os.path.isdir(profile):
        os.rename(profile,profile_dni)
        # si existe le cambiamos el nombre a dni
        print '-SI, EXISTE el profile '  + usuario + ' y se cambio el nombre a '  + dni
        print '--------DATOS DEL CSV----------'
        print 'usuario: ' + usuario
        print 'dni: ' + dni
        print 'mail: ' + mail
        # creo link simbolico en el profile
        os.symlink(path_profiles, path_profiles + usuario)

        pw = pwd.getpwnam('soporte')
        uid = pw.pw_uid
        gid = grp.getgrnam('soporte').gr_gid
        print 'pw >>>>', pw
        print 'uid >>>>', uid
        print 'gid >>>>', gid

        os.chown(profile_dni, 1001, 1001)

        profiles_mod +=1

    # reviso si existe el home del usuario en el path_home
    if os.path.isdir(home):
        os.rename(home,home_dni)
        # si existe le cambiamos el nombre a dni
        print '-SI, EXISTE el home '  + usuario + ' y se cambio el nombre a '  + dni
        print '--------DATOS DEL CSV----------'
        print 'usuario: ' + usuario
        print 'dni: ' + dni
        print 'mail: ' + mail

        # creo link simbolico en el home
        os.symlink(path_home, path_home + usuario)

        pw = pwd.getpwnam('soporte')
        uid = pw.pw_uid
        gid = grp.getgrnam('soporte').gr_gid
        print 'pw >>>>', pw
        print 'uid >>>>', uid
        print 'gid >>>>', gid
        # os.chown(dni, 1001, 1001)

        home_mod +=1

print 'Perfiles modificados ', profiles_mod
print 'home modificados ', home_mod
