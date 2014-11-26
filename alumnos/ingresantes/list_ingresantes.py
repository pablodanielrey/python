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
l.simple_bind("admin", "clave")

result = l.search_s('ou=people,dc=econo',ldap.SCOPE_SUBTREE, '(businessCategory=*)',['givenName','x-dcsys-dni','sn','x-dcsys-mail'])
for dn,r in result:
	mail = 'no tiene'
	if 'x-dcsys-mail' in r:
		mail = r['x-dcsys-mail'][0]
	print "%s,%s,%s,%s" % (r['x-dcsys-dni'][0],r['sn'][0],r['givenName'][0],mail)

l.unbind_s()
