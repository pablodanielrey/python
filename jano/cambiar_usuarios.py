# -*- coding: utf-8 -*-
import csv
import pwd
import grp
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# asigno la ruta donde estan los archivos a la variable path_profiles
path_home = '/media/jano/Archivos/python/python/jano/home/'
path_profiles = '/media/jano/Archivos/python/python/jano/home/samba/profiles/'

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

    # reviso si existe el home del usuario en el path_home
    if os.path.isdir(home):
        # me fijo si no es un link simbolico
        if not os.path.islink(home):
            # le cambiamos el nombre a dni
            os.rename(home,home_dni)
            print bcolors.WARNING, 'Existe el home ', usuario, 'y se renombro a ', dni, bcolors.ENDC
            print '--------DATOS DEL CSV----------'
            print 'usuario: ' + usuario
            print 'dni: ' + dni
            print 'mail: ' + mail
            print '-------------------------------'


            # cambio los permisos del directorio del usuario
            # os.chmod(home_dni, 0777)

            # me fijo cuales son el gid y uid del usuario,ejemplo soporte
            uid_home = pwd.getpwnam('manolo')[2]
            gid_home = grp.getgrnam('manolo')[2]
            uid_jano = pwd.getpwnam('jano')[2]
            print 'ID del usuario ', dni, '>>> ', uid_home
            print 'ID de grupo ', dni, '>>> ', gid_home
            print 'ID de de jano >>>', uid_jano

            print home_dni
            # cambio el propietario de usuario a dni
            os.chown(home_dni,uid_home,gid_home)

            # creo link simbolico en el home
            os.symlink(home_dni, path_home + usuario)

            home_mod +=1

    # reviso si existe el profile del usuario en el path_profiles
    if os.path.isdir(profile):
        # me fijo si no es un link simbolico
        if not os.path.islink(profile):
            # le cambiamos el nombre a dni
            os.rename(profile,profile_dni)
            print bcolors.WARNING, 'Existe el perfil ', usuario, 'y se renombro a ', dni, bcolors.ENDC
            print '--------DATOS DEL CSV----------'
            print 'usuario: ' + usuario
            print 'dni: ' + dni
            print 'mail: ' + mail
            print '-------------------------------'
            # cambio los permisos del directorio del usuario
            # os.chmod(profile_dni, 0777)

            # me fijo cuales son el gid y uid del usuario, ejemplo soporte
            uid_profile = pwd.getpwnam('manolo')[2]
            gid_profile = grp.getgrnam('manolo')[2]
            print 'ID del usuario ', dni, '>>> ', uid_profile
            print 'ID de grupo ', dni, '>>> ', gid_profile

            print profile_dni
            # cambio el propietario de usuario a dni
            os.chown(profile_dni,uid_profile,gid_profile)


            # creo link simbolico en el profile
            os.symlink(profile_dni, path_profiles + usuario)

            profiles_mod +=1

        print '\n'

print bcolors.BOLD, 'homes modificados ', home_mod, bcolors.ENDC
print bcolors.BOLD, 'Perfiles modificados ', profiles_mod, bcolors.ENDC
