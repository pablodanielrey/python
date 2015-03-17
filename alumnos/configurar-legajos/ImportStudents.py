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

with open('/tmp/sto.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for nombre, legajo, dni in reader:
            print "Nombre : ", nombre
#            print "Apellido : ", apellido
            print "Legajo : ", legajo
            print "Dni : ", dni

            suuid = str(uuid.uuid4())
            dn = 'x-dcsys-uuid=' + suuid + ',ou=people,dc=econo'

            try:
                result = l.search_s('ou=people,dc=econo',ldap.SCOPE_SUBTREE, '(x-dcsys-dni='+dni+")",['cn','x-dcsys-dni','sn','x-dcsys-uuid','x-dcsys-legajo'])

                for dn,attrs in result:
                    print "modificando %s " % dni
                    mod_attrs = [(ldap.MOD_REPLACE,'x-dcsys-legajo',legajo)]
                    l.modify_s(dn,mod_attrs)

            except ldap.LDAPError, e:
                print e

l.unbind_s()
