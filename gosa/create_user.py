import ldap
import ldap.modlist as modlist
import uuid
import sys


user = sys.argv[1]
passw = sys.argv[2]
dni = sys.argv[3]
name = sys.argv[4]
lastname = sys.argv[5]

try:
        l = ldap.initialize("ldap://127.0.0.1:3389")
        l.protocol_version = ldap.VERSION3
        l.simple_bind_s(user,passw);

        result = l.search_s("dc=econo",ldap.SCOPE_SUBTREE,"(uid=" + dni +")",["dn"])
	if (result != None) and (len(result) > 0):
		print "ya existe ese usuario"
		print result
		exit(1)

	username = name + "." + lastname

        result = l.search_s("dc=econo",ldap.SCOPE_SUBTREE,"(uid=" + username +")",["dn"])
	if (result != None) and (len(result) > 0):
		print "ya existe ese usuario"
		print result
		exit(1)


        result = l.search_s("dc=econo",ldap.SCOPE_SUBTREE,"(|(gidNumber=*)(uidNumber=*))",["gidNumber",'uidNumber'])
        lastNumber = 0
	if result != None:
	  for dn,n in result:
	      if 'gidNumber' in n:
		num = int(n['gidNumber'][0])
		if lastNumber < num:
		  lastNumber = num
	      if 'uidNumber' in n:
		num = int(n['uidNumber'][0])
		if lastNumber < num:
		  lastNumber = num


	uidN = str(lastNumber + 1)
	gid = str(lastNumber + 2)
	sambaSID = 'S-1-5-21-69815507-558479685-3467165442-' + uidN
	sambaGroupSID = 'S-1-5-21-69815507-558479685-3467165442-' + gid


	mod_attrs = [('sn', lastname),
		     ('givenName', name),
		     ('cn', name + " " + lastname),
		     ('uid', [username, dni]),
		     ('homeDirectory', '/home/' + username),
		     ('loginShell', '/bin/bash'),
		     ('uidNumber', uidN),
		     ('gidNumber', gid),
		     ('mail', username + "@econo.unlp.edu.ar"),
		     ('sambaSID',sambaSID),
		     ('sambaPrimaryGroupSID',sambaGroupSID),
		     ('sambaLMPassword',''),
		     ('sambaNTPassword',''),
		     ('sambaPwdCanChange','1'),
		     ('sambaAcctFlags','[UX          ]'),
		     ('userPassword',''),
		     ('shadowLastChange','14659'),
		     ('gosaMailServer','smtp'),
		     ('gosaMailDeliveryMode','[L]'),
		     ('objectClass', ['top','person','organizationalPerson','inetOrgPerson','posixAccount','shadowAccount','sambaSamAccount','gosaMailAccount'])
	]
	
	
	dn = "uid=" + username + ",ou=people,dc=econo"
        l.add_s(dn,mod_attrs)
                                                                                                                                                                                                                                             
        l.unbind_s()                                                                                                                                                                                                                         
                                                                                                                                                                                                                                             
except ldap.LDAPError, e:                                                                                                                                                                                                                    
        print e                              
