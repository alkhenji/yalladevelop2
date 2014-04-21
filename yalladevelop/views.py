''' This will be the Controller of the Application. Examples below. '''

# Urls and HttpResponses
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, render_to_response

# User forms
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission
from yalladevelop.forms import *
from django.utils.html import escape

# Authentication and Users
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.context_processors import csrf
from django.template import RequestContext

# Models
from yalladevelop.models import *

# Mailer
from django.core.mail import send_mail

# Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Other Imports
import random
from django.conf.urls import patterns, url


# Image Handlers
from base64 import b64decode
from django.core.files.base import ContentFile


# -------------------- Parameters Function -------------------------
# Function returns a dictionary of the variables
def getVariables(request,dictionary={}):
	user = request.user
	logged_in = request.user.is_authenticated()
	not_logged_in = not logged_in
	admin = request.user.is_staff
	if logged_in and not admin:
		user_is_company = UserProfile.objects.get(user=user).is_company
		user_profile = UserProfile.objects.get(user=user)
		is_premium = UserProfile.objects.get(user=user).is_premium
	elif admin:
		user_is_company = False
		user_profile = False
	else: #not logged in
		user_is_company = False
		user_profile = False
	if dictionary:
		dictionary['user'] = user
		dictionary['logged_in'] = logged_in
		dictionary['not_logged_in'] = not logged_in
		if logged_in and not admin:
			dictionary['is_company'] = UserProfile.objects.get(user=user).is_company
			dictionary['is_premium'] = UserProfile.objects.get(user=user).is_premium
		if logged_in and admin:
			dictionary['is_company'] = False
		return dictionary
	else:
		return {'user':user,'logged_in':logged_in,'not_logged_in':not_logged_in,'is_company':user_is_company, 'user_profile': user_profile}


def rankings(request):
	d = getVariables(request,dictionary={'page_name': "Rankings"})
	top_users = UserProfile.objects.filter(is_company=False).order_by('-points')[:10]
	top_companies = UserProfile.objects.filter(is_company=True).order_by('-points')[:10]
	
	top_projects = Project.objects.order_by('-likes')[:10]
	
	d['top_users'] = top_users
	d['top_companies'] = top_companies
	d['top_projects'] = top_projects
	
	return render(request,'yalladevelop/rankings.html',d)


def index(request):
	d = getVariables(request,dictionary={'page_name': "Home"})
	if Project.objects.all():
		d['featured_projects'] = Project.objects.filter(is_featured=True).order_by('?')[:6]
		d['hot_projects'] = Project.objects.all().order_by('-likes')[:3] # how many projects
		d['projects'] = Project.objects.filter(is_featured=True).order_by('?')[:5]
	if UserProfile.objects.filter(is_company=False):
		d['random_member'] = UserProfile.objects.filter(is_company=False).order_by('?')[:1][0]
	return render(request, 'yalladevelop/index.html', d)

@login_required
@csrf_exempt
def addProject(request):
	d = getVariables(request)
	if d['is_company']:
		return redirect('/')
	d['page_name'] = "Add Project"
	if request.method == "POST":
		form = AddForm(request.POST,request.FILES)
		if form.is_valid():
			image = request.FILES['image']
			name = form.cleaned_data['project_name']
			description = form.cleaned_data['description']
			money = form.cleaned_data['target_money']
			p = Project(name=name,user_id=request.user.id,target_money=money,description=description,image=image,mimetype=image.content_type)
			p.save()
			
			if len(request.FILES) > 1:
				image_file = request.FILES['image']
				mimetype = image_file.content_type
				projectId = p.id
				
				image = ProjectImage(image=image_file,mimetype=mimetype,projectId=projectId)
				image.save()
			
			url = '/project/%s' % str(p.id)
			return HttpResponseRedirect(url) # return to new project page
		else:
			form = AddForm()
			d['form'] = form
			return render(request, 'yalladevelop/addproject.html', d)
			# return HttpResponseRedirect('/addproject') # return to new project page
		return render(request, 'yalladevelop/addproject.html', d)
	else:
		form = AddForm()
		d['form'] = form
	return render(request, "yalladevelop/addproject.html", d)

@login_required
def editProject(request,project_id):
	try:
		project = Project.objects.get(id=project_id)
	except Exception:
		return HttpResponseRedirect('/')
	
	if project.completed:
		return HttpResponseRedirect('/')
	
	d = getVariables(request)
	d['project'] = project
	if request.method == "POST":
		form = EditForm(request.POST)
		if form.is_valid():
			form.update(d)
			return HttpResponseRedirect("/project/" + str(project.id))
	else:
		u = request.user
		up = d['user_profile']
		initial = {'project_name':project.name,'description':project.description}
		d['form'] = EditForm(initial=initial)
	return render(request, 'yalladevelop/project_settings.html', d)
	
def showProject(request,project_id=-1):
	d = getVariables(request,dictionary={'page_name': "Browse Projects"})
	if project_id > 0:
		project = Project.objects.filter(id=project_id)
		if project:
			project = project[0]
			d['page_name'] = "Project: %s" % project.name
			d['project'] = project
			d['owner'] = User.objects.get(id=project.user_id).username
			d['progress'] = min(int((float(project.money_collected) / float(project.target_money)) * 100),100)
			d['helpers'] = project.helpers.all()
			d['funders'] = project.funders.all()
			d['complete'] = project.money_collected >= project.target_money
			d['comments'] = Comment.objects.filter(project_id=project.id)
			
			if (d['complete']) and (not project.completed): #fixes any un-noticed payments
				project.completed = True
				project.save()
			
			if request.user.is_authenticated():
				user = request.user
				up = UserProfile.objects.get(user=user)
				d['userProfile'] = up
				
				projectLiked = Like.objects.filter(project_id=project.id,user_id=user.id)
				
				d['my_project'] = project.user_id == request.user.id

				d['username'] = user.username
				
				if projectLiked:
					d['liked'] = True
				else:
					d['liked'] = False
					
				if not d['is_company']:
					d['helped'] = up in project.helpers.filter(id=up.id)
			return render(request,'yalladevelop/project.html', d)
		else:
			return render(request, 'yalladevelop/404.html')
	elif project_id == -1:
		projects = Project.objects.all()
		d['projects'] = projects
		return render(request, 'yalladevelop/404.html')
	else:
		return render(request, 'yalladevelop/404.html')


def showProfile(request,profile_id=-1):
	d = getVariables(request,dictionary={'page_name': "Browse Profiles"})
	if profile_id == str(1):
		if request.user.is_staff:
			return redirect('/admin')
		else:
			return redirect('/')
	elif profile_id > 1:	
		userAccount = User.objects.get(id=profile_id)
		userProfile = UserProfile.objects.get(user=userAccount)
		if userProfile:
			skills = userProfile.skill.all()
			d['userAccount'] = userAccount
			d['userProfile'] = userProfile
			d['page_name'] = "%s's Profile" % userProfile.name
			d['my_page'] = False
			d['skills'] = skills
			if request.user.id == userAccount.id:
				d['my_profile'] = True
			else:
				d['my_profile'] = False
			# if UserImage.objects.filter(userId=userAccount.id):
			# 	d['has_image'] = True
			# else:
			# 	d['has_image'] = False
			return render(request,'yalladevelop/profile.html', d)
		else:
			return render(request, 'yalladevelop/404.html')
	elif profile_id == -1:
		return render(request, 'yalladevelop/allusers.html',d)
	else:
		return render(request, 'yalladevelop/404.html')
	
# -------------------- Authentication ----------------------
def signup(request):
	return render(request, 'yalladevelop/signup.html', {})

@csrf_exempt
def signup_user(request):
	if request.method == 'POST':
		form = UserCreateForm(request.POST,request.FILES)
		if form.is_valid():
			image = request.FILES['image']
			new_user = form.save(image=image)
			new_user = authenticate(username=request.POST['username'],password=request.POST['password1'])
			login(request, new_user)
			
			return HttpResponseRedirect(reverse('index'))
	else:
		form = UserCreateForm()
	return render(request, "yalladevelop/signup.html", {'form': form,'usersignup':True})

@csrf_exempt
def signup_company(request):
	if request.method == 'POST':
		form = CompanyCreateForm(request.POST,request.FILES)
		
		if form.is_valid():
			image = request.FILES['image']
			new_user = form.save(image=image)
			new_user = authenticate(username=request.POST['username'],password=request.POST['password1'])
			login(request, new_user)
			
			return HttpResponseRedirect(reverse('index'))
	else:
		form = CompanyCreateForm()
	return render(request, "yalladevelop/signup.html", {'form': form,'usersignup':False})

def login_user(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username,password=password)
	if user:
		return render(request, 'yalladevelop/index.html')
	else:
		return HttpResponseRedirect('/')

		
def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')


# -------------------- Static Pages -------------------------
def about(request):
	d = getVariables(request)
	return render(request, 'yalladevelop/about.html', d)


def randomPasswordGenerator():
	alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*"
	password_length = 10
	new_password = ""
	for i in range(password_length):
		c = random.randrange(len(alphabet))
		new_password += alphabet[c]
	return new_password


def forgotPassword(request):
	d = getVariables(request)
	if request.method == "POST":
		form = ForgotForm(request.POST)
		if form.is_valid():
			# fetch the username by email
			email = form.cleaned_data['email']
			user = User.objects.filter(email=email)
			if user:
				user = user[0]			
				new_password = randomPasswordGenerator()
				user.set_password(new_password)
				subject = "YallaDevelop - Password Reset"
				message = "Password have been reset, your new password is %s" % new_password
				sender = "noreply@yalladevelop.com"
				recipients = ['al.khenji@gmail.com']
				send_mail(subject,message,sender,recipients)
				user.save()
				return HttpResponseRedirect('/')
		else:
			d['form'] = form
			return render(request, 'yalladevelop/forgotpassword.html', d)
		form = ForgotForm()
		d['form'] = form
		return render(request, 'yalladevelop/forgotpassword.html', d)
	else:
		form = ForgotForm()
		d['form'] = form
	return render(request, "yalladevelop/forgotpassword.html", d)

def contact(request):
	d = getVariables(request)
	if request.method == "POST":
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']
			sender = form.cleaned_data['sender']
			cc_myself = form.cleaned_data['cc_myself']
			recipients = ['al.khenji@gmail.com']
			if cc_myself:
				recipients.append(sender)
			send_mail(subject,message,sender,recipients)
			return HttpResponseRedirect('/')
		else:
			d['form'] = form
		return render(request, 'yalladevelop/contact.html', d)
	else:
		form = ContactForm()
		d['form'] = form
	return render(request, "yalladevelop/contact.html", d)


def allprojects(request):
	d = getVariables(request)
	projects = Project.objects.all()
	paginator = Paginator(projects, 25) # Show 25 projects per page
	page = request.GET.get('page')
	try:
		projects = paginator.page(page)
	except PageNotAnInteger:
		projects = paginator.page(1)
	except EmptyPage:
		projects = paginator.page(paginator.num_pages)
	d['projects'] = projects
	d['paginator'] = paginator
	return render_to_response('yalladevelop/allprojects.html',d)



def allusers(request):
	d = getVariables(request)
	users = UserProfile.objects.filter(is_company=False)
	paginator = Paginator(users, 9) # Show 25 projects per page
	page = request.GET.get('page')
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)
	d['users'] = users
	d['paginator'] = paginator
	

	return render_to_response('yalladevelop/allusers.html',d)
	
def allcompanies(request):
	d = getVariables(request)
	users = UserProfile.objects.filter(is_company=True)
	paginator = Paginator(users, 25) # Show 25 projects per page
	page = request.GET.get('page')
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)
	d['users'] = users
	d['paginator'] = paginator
	return render_to_response('yalladevelop/allcompanies.html',d)


@login_required
def track(request):
	if request.user.is_staff:
		return HttpResponseRedirect('/')
	d = getVariables(request)
	u = d['user']
	up = UserProfile.objects.get(user_id=u.id)

	if not d['is_company']:
		d['my_projects'] = Project.objects.filter(user_id=u.id)
		d['helping'] = Project.objects.filter(helpers=up.id)
	d['funding'] = Project.objects.filter(funders=up.id)
	
	return render_to_response('yalladevelop/track.html',d)


def explore(request):
	d = getVariables(request)
	if Project.objects.all():
		projects = Project.objects.all().order_by('?')[:9]
		d['projects'] = projects
	return render_to_response('yalladevelop/explore.html',d)

def faq(request):
	d = getVariables(request)
	return render(request, 'yalladevelop/faq.html', d)

def help(request):
	d = getVariables(request)
	return render(request, 'yalladevelop/help.html', d)

def privacy(request):
	d = getVariables(request)
	return render(request, 'yalladevelop/privacy.html', d)

def sitemap(request):
	d = getVariables(request)
	return render(request, 'yalladevelop/sitemap.html', d)

def privacy(request):
	d = getVariables(request)
	return render(request, 'yalladevelop/privacy.html', {})

def terms(request):
	d = getVariables(request)
	return render(request, 'yalladevelop/terms.html', {})

def test(request):
	d = getVariables(request)
	return render(request, 'yalladevelop/111.html', {})

def dhelp(request):
	return render(request,'yalladevelop/components.html')

def userorcompany(request):
	d = getVariables(request)
	return render(request, 'yalladevelop/userorcompany.html', {})

@login_required
def profileSettings(request):
	d = getVariables(request)
	if request.method == "POST":
		if d['user_profile'].is_company:
			form = CompanyUpdateForm(request.POST)
		else: #if user
			form = UserUpdateForm(request.POST)
		if form.is_valid():
			form.update(d)
			return redirect("/profile/" + str(request.user.id))
		else:
			d['form'] = form
			return render(request, 'yalladevelop/profile_settings.html', d)
	else:
		u = request.user
		up = d['user_profile']
		if d['user_profile'].is_company:
			d['form'] = CompanyUpdateForm(initial={'name':up.name,'email':u.email})
		else:
			initial = {'name':up.name,'email':u.email}
			letter = lambda i: "abcdefghijklmnopqrstuvwxyz"[i-1] #takes a number, returns character
			for skill in Skill.objects.all():
				if skill not in up.skill.all():
					initial[letter(skill.id)] = False
				else:
					initial[letter(skill.id)] = True
			d['form'] = UserUpdateForm(initial=initial)
	return render(request, 'yalladevelop/profile_settings.html', d)

def search_skills(request,skill_id=0):
	d = getVariables(request)
	if skill_id == 0:
		d['skills'] = Skill.objects.all()
		return render_to_response('yalladevelop/search_skills.html',d)
	else:
		skill = Skill.objects.filter(id=skill_id)
		if skill:
			skill = skill[0]
			users = UserProfile.objects.filter(skill=skill)
			paginator = Paginator(users,2) # showing 25 users
			page = request.GET.get('page')
			
			try:
				users = paginator.page(page)
			except PageNotAnInteger:
				users = paginator.page(1)
			except EmptyPage:
				users = paginator.page(paginator.num_pages)
			
			d['users'] = users
			d['skill'] = skill
			
			return render_to_response('yalladevelop/search_skills.html',d)
		else: #if skill is not found
			return search_skills(request,skill_id=0)


# -------------------- Functions -------------------------
@login_required
def postComment(request):
	post = request.POST
	comment = escape(post['comment'])
	userId = post['userId']
	username = post['username']
	project_id = post['projectId']
	project_owner = Project.objects.get(id=project_id).user_id
	
	if len(comment)>1:
		newComment = Comment(project_id=project_id,comment=comment,username=username,user_id=userId,project_owner=project_owner)
		newComment.save()
	url = "/project/"+str(project_id)+"/"
	return HttpResponseRedirect(url)
	
	

@login_required
def likeProject(request,project_id):
	like = Like.objects.filter(project_id=project_id,user_id=request.user.id)
	project = Project.objects.filter(id=project_id)
	if not project:
		return HttpResponseRedirect("/")
	else:
		project = project[0]
		user = request.user
		liked = Like.objects.filter(project_id=project.id,user_id=user.id)		
		if not liked:
			newLike = Like(project_id=project.id,user_id=user.id)
			newLike.save()
			project.likes += 1
			project.save()
		url = '/project/%s' % str(project.id)
		return HttpResponseRedirect(url) # return to project page

@login_required
def helpProject(request,project_id):
	project = Project.objects.filter(id=project_id)
	if project:
		project = project[0]
		user = request.user
		up = UserProfile.objects.get(user=user)
		
		if up.skill.count() > 0:
			helping = up in project.helpers.filter(id=up.id)
			if not helping:
				# add user to helpers
				project.helpers.add(up)
				url = '/project/%s' % str(project.id)
				return HttpResponseRedirect(url)
			else: # if helping
				# remove user from helpers
				project.helpers.remove(up)
				url = '/project/%s' % str(project.id)
				return HttpResponseRedirect(url)
		else: # user doesn't have any skills!!! --------------------------- should redirect to profile page to add skills
			url = '/project/%s' % str(project.id)
			return HttpResponseRedirect(url)
		
def donate(request,project_id=False):
	if project_id == False:
		return HttpResponseRedirect('/')
	try:
		project = Project.objects.get(id=project_id)
	except Exception:
		return HttpResponseRedirect('/')
	
	d = getVariables(request)
	d['project'] = project
	
	try: # don't accept payments for projects that do not have an owner
		d['owner'] = User.objects.get(id=project.user_id)
	except Exception:
		return HttpResponseRedirect('/')
		
	if project.completed: #don't accept payments for completed projects
		return HttpResponseRedirect('/')
	
	if request.method == "POST":
		form = DonateForm(request.POST)
		if form.is_valid():
			if project.money_collected < project.target_money:
				project.money_collected += form.cleaned_data['amount']
				
				if (request.user.is_authenticated()) and (not request.user.is_staff):
					user = request.user
					up = UserProfile.objects.get(user=user)
					project.funders.add(up)
					up.points += form.cleaned_data['amount']
					up.save()
				
			if project.money_collected >= project.target_money:
				project.completed = True
			
			project.save()
			return HttpResponseRedirect('/project/'+str(project.id)+'/')
		else:
			form = DonateForm()
			d['form'] = form
		return render(request, 'yalladevelop/donate.html', d)
	else:
		form = DonateForm()
		d['form'] = form
	return render(request, "yalladevelop/donate.html", d)

# Reading profile picture
def getProfilePicture(request,user_id):
	u = User.objects.get(id=user_id)
	e = UserProfile.objects.get(user=u)
	return HttpResponse(e.image.read(), mimetype=e.mimetype)

# Reading the project picture
def getProjectPicture(request,project_id):
	p = Project.objects.get(id=project_id)
	return HttpResponse(p.image.read(), mimetype=p.mimetype)

def user_upload(request):
	pass