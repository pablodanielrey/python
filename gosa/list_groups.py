import ldap
import ldap.modlist as modlist
import uuid
import sys


user = sys.argv[1]
passw = sys.argv[2]

try:
        l = ldap.initialize("ldap://127.0.0.1:3389")
        l.protocol_version = ldap.VERSION3
        l.simple_bind_s(user,passw);

        result = l.search_s("ou=groups,dc=econo",ldap.SCOPE_SUBTREE,"(cn=*)",["cn","gosaMailAlternateAddress","acl","memberUid"])
	if result == None:
		exit(1)

	
	for dn,g in result:

		if 'memberUid' not in g:
			continue

		print "\n\n"
		print "Grupo : " + str(g['cn'])
		
		if 'gosaMailAlternateAddress' in g:
			mail = "     mail : "
			for m in g['gosaMailAlternateAddress']:
				print mail + m

		if 'acl' in g:
			permisos = "     perm : "
			for p in g['acl']:
				print(permisos + p)

		if 'memberUid' in g:
			miembros = "     miembro : "
			for m in g['memberUid']:
				print(miembros + m)


        l.unbind_s()                                                                                                                                                                                                                         
                                                                                                                                                                                                                                             
except ldap.LDAPError, e:                                                                                                                                                                                                                    
        print e                              
