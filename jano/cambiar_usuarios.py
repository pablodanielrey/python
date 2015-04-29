# -*- coding: utf-8 -*-
import csv, pwd, grp, os
import logging
import re
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def renombrarCarpeta(home,dni,d):

    if os.path.exists(dni):
        return 0

    if not os.path.exists(home):
        os.mkdir(home)

    # reviso si existe el home del usuario en el path_home
    if os.path.isdir(home):
        # me fijo si no es un link simbolico
        if not os.path.islink(home):
            # le cambiamos el nombre a dni
            os.rename(home,dni)

    # cambio los permisos del directorio del usuario
    # os.chmod(home_dni, 0777)

    # me fijo cuales son el gid y uid del usuario,ejemplo soporte
    uid_home = pwd.getpwnam(d)[2]
    gid_home = grp.getgrnam(d)[2]
    os.chown(home_dni,uid_home,gid_home)

    # creo link simbolico en el home
    os.symlink(dni, home)

    return 1


logging.basicConfig(level=logging.DEBUG)

extraerParteLocal = re.compile('(.+)@(.+)')


# asigno la ruta donde estan los archivos a la variable path_profiles
path_home = '/home/'
path_profiles = '/home/samba/profiles/'

profiles_mod = 0
home_mod = 0

# abrimos el archivo csv con permisos de lectura
#reader = csv.reader(sys.stdin)
# hago un for para recorrer las filas del archivo csv

dni = sys.argv[1]
mail = sys.argv[2]
#for dni,mail in reader:
grupos = extraerParteLocal.match(mail)
usuario = grupos.group(1)

profile = path_profiles + usuario
home = path_home + usuario
profile_dni = path_profiles + dni
home_dni = path_home + dni

logging.debug('{} {} {} {} {} {}'.format(dni,usuario,home,profile,home_dni,profile_dni))

home_mod = home_mod + renombrarCarpeta(home,home_dni,dni)
profiles_mod = profiles_mod + renombrarCarpeta(profile,profile_dni,dni)

logging.debug('homes modificados {}'.format(home_mod))
logging.debug('Perfiles modificados {}'.format(profiles_mod))
