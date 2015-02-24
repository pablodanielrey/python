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

with open('/tmp/personas-con-mail.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for nombre, apellido, dni, mail in reader:
            print "Nombre : ", nombre
            print "Apellido : ", apellido
            print "Dni : ", dni
	    print "Mail : ", mail
            
            suuid = str(uuid.uuid4())
            dn = 'x-dcsys-uuid=' + suuid + ',ou=people,dc=econo' 
            
            person = {}
            person['objectClass'] = ['top','person','inetOrgPerson','x-dcsys-entidad','x-dcsys-persona']
            person['x-dcsys-uuid'] = suuid
            person['x-dcsys-dni'] = dni
            person['uid'] = dni
            person['cn'] = nombre + ' ' + apellido
            person['givenName'] = nombre
            person['sn'] = apellido
            person['userPassword'] = dni
	    person['x-dcsys-mail'] = mail

            try:
                result = l.search_s('ou=people,dc=econo',ldap.SCOPE_SUBTREE, '(x-dcsys-dni='+dni+")",['cn','x-dcsys-dni','sn','x-dcsys-uuid'])
                print result
                if result == []:
                    print "agregando %s " % dn 
                    print person
                    l.add_s(dn,modlist.addModlist(person))
                
            except ldap.LDAPError, e:
                print e

l.unbind_s()
