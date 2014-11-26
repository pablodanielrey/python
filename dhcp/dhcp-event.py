#!/usr/bin/env python
import psycopg2
import os, sys

host = ''


#ClientIP, ClientMac, host-decl-name
if (len(sys.argv) > 1):

	command = sys.argv[1]
	clientIP = sys.argv[2]
	clientMac = sys.argv[3]
	hostname = sys.argv[4]

	if command == "commit":
		f = open("/tmp/leases",'a')
		s = "Leased: %s to %s\n" % (clientIP, hostname)
		f.write(s)
		f.flush()
		f.close()

		db = psycopg2.connect(host=host, user="dhcp", password="dhcp", dbname="dhcp")
                cursor = db.cursor()
		cursor.execute("delete from leases where ip = %s",[clientIP])
		cursor.execute("INSERT INTO leases (ip,mac,hostname) VALUES (%s,%s,%s)", [clientIP,clientMac,hostname])
#		pp.pprint(cursor.__dict__)
		cursor.close()
		db.commit()
		db.close()

	elif command == "release":
		f = open("/tmp/leases",'a')
		s = "Released: %s from %s\n" % (clientIP, hostname)
		f.write(s)
		f.flush()
		f.close()

		db = psycopg2.connect(host=host, user="dhcp", password="dhcp", dbname="dhcp")
                cursor = db.cursor()
		cursor.execute("DELETE FROM records WHERE content = %s AND name = %s",[clientIP,hostname])
		#pp.pprint(cursor.__dict__)
		db.commit()
		db.close()

	elif command == "expiry":
		f = open("/tmp/leases",'a')
                s = "Expired: %s from %s\n" % (clientIP, hostname)
                f.write(s)
                f.flush()
                f.close()
	
		db = psycopg2.connect(host=host, user="dhcp", password="dhcp", dbname="dhcp")
                cursor = db.cursor()
		cursor.execute("DELETE FROM records WHERE content = %s AND name = %s",[clientIP,hostname])
		#pp.pprint(cursor.__dict__)
		db.commit()
		db.close()
	
