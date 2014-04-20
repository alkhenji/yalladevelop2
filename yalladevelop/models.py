#Database Models
''' This will be the database model '''

from django.db import models
from django import forms
from django.contrib.auth.models import User
import os

class Skill(models.Model):
	# id built in
	'''
	a = "Python, Django"
	b = "Java, Javascript"
	c = "C, C++, C#"
	d = "Ruby, Ruby on Rails"
	e = "HTML, CSS"
	f = "PHP"
	g = "Perl"
	h = "ASP & VBScript"
	i = "Adobe Photoshop, Illustrator"
	j = "SQL Databases"
	'''
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	def __unicode__(self):
		return self.name

class UserImage(models.Model):
	image = models.ImageField(upload_to='uploads/')
	mimetype = models.CharField(max_length=20)
	userId = models.IntegerField() # Id of the user it belongs to
	def __unicode__(self):
		return "Image belongs to user: "+str(self.userId)

class ProjectImage(models.Model):
	image = models.ImageField(upload_to='uploads/')
	mimetype = models.CharField(max_length=20)
	projectId = models.IntegerField()
	def __unicode__(self):
		return "Image belongs to project: "+str(self.projectId)

class Like(models.Model):
	project_id = models.IntegerField()
	user_id = models.IntegerField()
	def __unicode__(self):
		user_id = str(self.user_id)
		project_id = str(self.project_id)
		return "User %s likes Project %s" % (user_id, project_id)

class UserProfile(models.Model):
	# firstName Already Built in
	# lastName Already Built in
	# email Already built in
	# password already built in
	# is_staff - Can access admin site?
	# is_active - Designates whether this user is active or not
	is_premium = models.BooleanField(default=False)
	is_company = models.BooleanField(default=False)
	skill = models.ManyToManyField(Skill)
	user = models.ForeignKey(User, unique=True)
	name = models.CharField(max_length=200)
	points = models.IntegerField(default=0)
	image = models.ImageField(upload_to='uploads/')
	mimetype = models.CharField(max_length=20)
	def __unicode__(self):
		return self.name


class Comment(models.Model):
	project_id = models.IntegerField()
	project_owner = models.IntegerField() # id of userProfile of the owner
	username = models.CharField(max_length=200)
	user_id = models.IntegerField() # id of the comment poster
	comment = models.CharField(max_length=200)


class Project(models.Model):
	user_id = models.IntegerField(null=False) # can be used to change owner of project later
	name = models.CharField(max_length=200)
	date_published = models.DateField(auto_now_add=True)
	date_completed = models.DateField(null=True)
	likes = models.IntegerField(default=0)
	target_money = models.IntegerField(null=False)
	money_collected = models.IntegerField(default=0)
	description = models.CharField(max_length=200)
	completed = models.BooleanField(default=False)
	is_featured = models.BooleanField(default=False)
	helpers = models.ManyToManyField(UserProfile,related_name="helper")
	funders = models.ManyToManyField(UserProfile,related_name="funder")
	image = models.ImageField(upload_to='uploads/')
	mimetype = models.CharField(max_length=20)
	def __unicode__(self):
		return self.name

class Payment(models.Model):
	user = models.ForeignKey(User, unique=False,null=True)
	project = models.ForeignKey(Project, unique=False,null=False)
	amount = models.IntegerField()
	def __unicode__(self):
		if user:
			return "User %s paid %s to project %s" % (str(user.id), str(amount), str(project.id))
		else:
			return "Payment of %s to project %s" % (str(amount), str(project.id))