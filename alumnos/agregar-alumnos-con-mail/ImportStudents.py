'''
Created on 19/12/2013

@author: pablo
'''

import csv
import ldap
import ldap.modlist as modlist
import uuid


l = ldap.initialize("ldap://127.0.0.1:3389")
l.protocol_version = ldap.VERSION3
l.simple_bind("cn=admin,dc=econo", "pcucqccp")

with open('/tmp/alumnos-con-mail.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for dni, legajo, nombre, apellido, mail in reader:
            print "Nombre : ", nombre
            print "Apellido : ", apellido
            print "Legajo : ", legajo
            print "Dni : ", dni
	        print "Mail : ", mail

            suuid = str(uuid.uuid4())
            dn = 'x-dcsys-uuid=' + suuid + ',ou=people,dc=econo'

            person = {}
            person['objectClass'] = ['top','person','inetOrgPerson','x-dcsys-entidad','x-dcsys-persona','x-dcsys-estudiante']
            person['x-dcsys-uuid'] = suuid
            person['x-dcsys-dni'] = dni
            person['x-dcsys-legajo'] = legajo
            person['uid'] = dni
            person['cn'] = nombre + ' ' + apellido
            person['givenName'] = nombre
            person['sn'] = apellido
            person['userPassword'] = dni[-4:]
	        person['businessCategory'] = 'ingresante'
	        person['x-dcsys-mail'] = mail

            try:
                result = l.search_s('ou=people,dc=econo',ldap.SCOPE_SUBTREE, '(x-dcsys-dni='+dni+")",['cn','x-dcsys-dni','sn','x-dcsys-uuid','x-dcsys-mail'])
                print result
                if result == []:
                    print "agregando %s " % dni
                    print person
                    l.add_s(dn,modlist.addModlist(person))
                else:
                    for dn,attrs in result:
                        mod_attrs = []
                        if 'x-dcsys-mail' in attrs:
                            mod_attrs = [(ldap.MOD_REPLACE,'x-dcsys-legajo',legajo)]
                        else:
                            mod_attrs = [(ldap.MOD_REPLACE,'x-dcsys-legajo',legajo),(ldap.MOD_REPLACE,'x-dcsys-mail','correo alternativo pendiente')]

                        print "modificando %s " % dni
                        l.modify_s(dn,mod_attrs)


            except ldap.LDAPError, e:
                print e

l.unbind_s()
