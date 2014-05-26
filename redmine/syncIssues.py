import uuid
import psycopg2


class RProject:
	def __init__(self, id, parent_id, name, desc):
		self.id = id
		self.parent_id = parent_id
		self.name = name
		self.desc = desc


class RIssue:
	def __init__(self, id, project_id, subject, desc, status_id, assigned_mail, author_mail, created_on, updated_on, start_date, parent_id, root_id):
		self.id = id
		self.project_id = project_id
		self.subject = subject
		self.desc = desc
		self.status_id = status_id
		self.assigned_mail = assigned_mail
		self.author_mail = author_mail
		self.created_on = created_on
		self.updated_on = updated_on
		self.start_date = start_date
		self.parent_id = parent_id
		self.root_id = root_id

	def __str__(self):
		return self.author_mail + " -- " + self.assigned_mail + " -- " + self.subject


	""" lee y retorna una lista de RIssues de la base """
	@staticmethod
	def read(cur, projects):
		sql = "select id,tracker_id, project_id, subject, description, due_date, category_id, status_id, assigned_to_id, priority_id, fixed_version_id, author_id, created_on, updated_on, start_date, done_ratio, parent_id, root_id from issues"
		cur.execute(sql);
		rows = cur.fetchall()

		count = 0
		for id, tracker_id, project_id, subject, desc, due_date, category_id, status_id, assigned_to_id, priority_id, fixed_version_id, author_id, created_on, updated_on, start_date, done_ratio, parent_id, root_id in rows:

			if author_id == None:
				continue

			if assigned_to_id == None:
				continue

			sql = "select mail from users where id = " + str(author_id)
			cur.execute(sql);
			rows2 = cur.fetchall();
			author_mail = rows2[0][0];
			
			if "@" not in author_mail:
				continue
			
                        sql = "select mail from users where id = " + str(assigned_to_id)
                        cur.execute(sql);
                        rows2 = cur.fetchall();
                        assigned_mail = rows2[0][0];

			if "@" not in assigned_mail:
				continue

			rissue = RIssue(id,project_id,subject,desc,status_id, assigned_mail, author_mail, created_on, updated_on, start_date, parent_id, root_id)
			print rissue

			count = count + 1
		
		print count



try:
	con2 = psycopg2.connect(database='redmine_default', host='127.0.0.1', port='5433', user='', password='')
# 	con = psycopg2.connect(database='redmine251', host='127.0.0.1', user='usuario', password='clave')

	cur = con2.cursor();
	RIssue.read(cur,[])

	cur.close();
	con2.close();
		
except psycopg2.DatabaseError, e:
    print 'Error %s' % e    
    sys.exit(1)	
	


