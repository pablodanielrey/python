import ldap
import ldap.modlist as modlist
import uuid
import sys


user = sys.argv[1]
passw = sys.argv[2]
cn = sys.argv[3]
dni = sys.argv[4]

try:
        l = ldap.initialize("ldap://127.0.0.1:3389")
        l.protocol_version = ldap.VERSION3
        l.simple_bind_s(user,passw);

        result = l.search_s("dc=econo",ldap.SCOPE_SUBTREE,"(uid=" + dni +")",["dn","uid","mail","x-dcsys-mail"])
	if result == None:
		print "No existe ese usuario"
		exit(1)

	
	dn, attrs = result[0]
	
	mail = ""
	if "x-dcsys-mail" in attrs:
		mail = attrs["x-dcsys-mail"][0]

	if "mail" in attrs:
		mail = attrs["mail"][0]
	
	
        result = l.search_s("dc=econo",ldap.SCOPE_SUBTREE,"(cn=" + cn +")",["dn","acl","memberUid"])

        if result == None:
                print "Ningun grupo"
                exit(1)                                                                                                                                                                                            
        
	dn, groupAttrs = result[0]

	acls = groupAttrs['acl']
	for acl in acls:
		if acl.find(mail) != -1:
			acls.remove(acl)
			break
		

	members = groupAttrs['memberUid']
	for uid in attrs['uid']:
		if uid in members:
			members.remove(uid)

        mod_attrs = [(ldap.MOD_REPLACE,'acl',acls),(ldap.MOD_REPLACE,'memberUid',members)]                                                                                                                                                                     

	print dn
	print mod_attrs

        l.modify_s(dn,mod_attrs)
	print mod_attrs
        print dn                                                                                                                                                                                 
                                                                                                                                                                                                                                             
        l.unbind_s()                                                                                                                                                                                                                         
                                                                                                                                                                                                                                             
except ldap.LDAPError, e:                                                                                                                                                                                                                    
        print e                              
