import ldap
import ldap.modlist as modlist
import uuid
import sys


user = sys.argv[1]
passw = sys.argv[2]
dn = sys.argv[3]

try:
        l = ldap.initialize("ldap://127.0.0.1:3389")
        l.protocol_version = ldap.VERSION3
        l.simple_bind_s(user,passw);

	l.delete_s(dn)
                                                                                                                                                                                                                                             
        l.unbind_s()                                                                                                                                                                                                                         
                                                                                                                                                                                                                                             
except ldap.LDAPError, e:                                                                                                                                                                                                                    
        print e                              
