import datetime
import sys
import uuid
import psycopg2
from redmine import Redmine

''' retorna un proyecto del redmine obtenido por rest dado por el nombre '''
def getProject(name, redmine):
	prjs = redmine.project.all()
	for pj in prjs:
		if pj.name == name:
			return pj
	return None


''' retorna una persona del redmine dado por el mail '''
def getPerson(mail, redmine):
	persons = redmine.user.all()
	for person in persons:
		if person.mail == mail:
			return person
	return None

''' retorna un status del redmine dado por el nombre '''
def getStatus(name, redmine):
	statuses = redmine.status.all()
	for status in statuses:
		if status.name == name:
			return status
	return None









class RProject:
	def __init__(self, sid, parent_id, name, desc):
		self.id = sid
		self.parent_id = parent_id
		self.name = name
		self.desc = desc

	def __str__(self):
		return str(self.id) + " " + self.name + " " + str(self.parent_id)

	@staticmethod
	def read(cur):
		sql = "select id,name,description,parent_id from projects where parent_id = 2"
		cur.execute(sql);
		rows = cur.fetchall();
		projects = []
		for sid,name,desc,p_id in rows:
			rp = RProject(sid,p_id,name,desc)
			projects.append(rp)

		return projects


	''' obtiene un projecto de la lista de proyectos por id '''
	@staticmethod
	def getProject(projects,sid):
		for prj in projects:
			if prj.id == sid:
				return prj
		return None


	def write(self,redmine):
		sid = uuid.uuid4().__str__().replace('-','')
		redmine.project.create(name=self.name, identifier=sid, description=self.desc, is_public=True, parent_id=13, inherit_members=True)



class RUser:
	@staticmethod
	def getMail(sid, cur):
		sql = "select mail from users where id = " + str(sid)
		cur.execute(sql);
		rows2 = cur.fetchall();
		mail = rows2[0][0];
		return mail


class RIssue:
	def __init__(self, sid, project_name, subject, desc, status_name, assigned_mail, author_mail, created_on, updated_on, start_date, parent_id, root_id):
		self.id = sid
		self.project_name = project_name
		self.subject = subject
		self.desc = desc
		self.status_name = status_name
		self.assigned_mail = assigned_mail
		self.author_mail = author_mail
		self.created_on = created_on
		self.updated_on = updated_on
		self.start_date = start_date
		self.parent_id = parent_id
		self.root_id = root_id

	def __str__(self):
		return self.author_mail + " -- " + self.assigned_mail + " -- " + self.subject + " -- " + self.project_name


	""" lee y retorna una lista de RIssues de la base """
	@staticmethod
	def read(cur, projects):
		sql = "select id,tracker_id, project_id, subject, description, due_date, category_id, status_id, assigned_to_id, priority_id, fixed_version_id, author_id, created_on, updated_on, start_date, done_ratio, parent_id, root_id from issues"
		cur.execute(sql);
		rows = cur.fetchall()

		count = 0
		issues = []
		for sid, tracker_id, project_id, subject, desc, due_date, category_id, status_id, assigned_to_id, priority_id, fixed_version_id, author_id, created_on, updated_on, start_date, done_ratio, parent_id, root_id in rows:

			if (assigned_to_id == None) or (author_id == None) or (subject == None) or (desc == None) or (project_id == None) or (status_id == None):
				continue
			
			author_mail = RUser.getMail(author_id, cur)
			if "@" not in author_mail:
				continue

			assigned_mail = RUser.getMail(assigned_to_id,cur)
			if "@" not in assigned_mail:
				continue

#			''' el status es distinto de cerrada '''
#			if status_id != 5:
#				continue
#			status_name = 'Cerrada'
#			status_name = RStatus.getName(status_id,cur)
			
			prj = RProject.getProject(projects, project_id)
			if prj == None:
				''' no es una tarea de las de los grupos que pase '''
				continue
			
			project_name = prj.name

			print("%d -- Leyendo:  %s  | Proyecto:  %s | Autor: %s | Asignado a : %s | Fecha C: %s" % (count,subject,project_name, author_mail, assigned_mail,created_on))

			print('date class : %s' % created_on.__class__.__name__)
			
			
			rissue = RIssue(sid,project_name,subject,desc,status_id, assigned_mail, author_mail, created_on, updated_on, start_date, parent_id, root_id)
			issues.append(rissue)
		
			count = count + 1
		
		return issues



	''' escribe dentro del redmine mediante la api rest el issue que representa este objeto '''
	def write(self,redmine):
		
		proj = getProject(self.project_name, redmine)
		''' status = getStatus(self.status_name, redmine) '''
		author = getPerson(self.author_mail, redmine)
		if author == None:
			return
		
		assigned = getPerson(self.assigned_mail, redmine)
		if assigned == None:
			return


#		status = getStatus(self.status_name,redmine)
#		if status == None:
#			return
		
		'''
		issue = redmine.issue.new();
		issue.project_id = proj.id
		issue.subject = self.subject
		issue.description = self.desc
		issue.status_id = self.status_name
		issue.is_private = False
		issue.created_on = self.created_on
		issue.updated_on = self.updated_on
		issue.done_ratio = 100
		issue.assigned_to_id = assigned.id
		issue.save()
		'''
		
		redmine.issue.create(project_id=proj.id, 
							subject=self.subject, 
							description=self.desc, 
							status_id=self.status_name, 
							is_private=False, 
							created_on=self.created_on, 
							updated_on=self.updated_on, 
							done_ratio=100,
							assigned_to_id=assigned.id)
		
		

try:
	redmine = Redmine("https://redmine-comp.econo.unlp.edu.ar",username="",password="", requests={'verify':False})

	con2 = psycopg2.connect(database='redmine_default', host='163.10.17.100', port='5432', user='', password='')
	cur = con2.cursor()

	projects = RProject.read(cur)

	'''
 	ya escribi los proyectos que me interezaba 	
	for pr in projects:
		pr.write(redmine)
	'''

	issues = RIssue.read(cur, projects)
	for issue in issues:
		print(issue)
		issue.write(redmine)

	cur.close();
	con2.close();
		
except psycopg2.DatabaseError as e:
	print('Error %s' % e)    
	sys.exit(1)	
	


