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

result = l.search_s('ou=people,dc=econo',ldap.SCOPE_SUBTREE, '(businessCategory=*)',['givenName','x-dcsys-dni','sn','x-dcsys-mail','x-dcsys-legajo'])
for dn,r in result:
	mail = 'no tiene'
	if 'x-dcsys-mail' in r:
		mail = r['x-dcsys-mail'][0]
	if 'x-dcsys-legajo' in r:
		legajo = r['x-dcsys-legajo'][0]
	print "%s;%s;%s;%s;%s" % (r['x-dcsys-dni'][0],r['sn'][0],r['givenName'][0],legajo,mail)

l.unbind_s()
