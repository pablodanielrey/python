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

        result = l.search_s("ou=people,dc=econo",ldap.SCOPE_SUBTREE,"(uid=*)",["uid","mail"])
	if result == None:
		exit(1)

	
	for dn,g in result:

		print "\n"
		print g['uid']
		if 'mail' in g:
			print g['mail']

        l.unbind_s()                                                                                                                                                                                                                         
                                                                                                                                                                                                                                             
except ldap.LDAPError, e:                                                                                                                                                                                                                    
        print e                              
