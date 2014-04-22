from django import forms
#from django.forms import
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from yalladevelop.models import Skill, UserProfile

from django.core.mail import send_mail

class ContactForm(forms.Form):
	name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Your Name"}))
	sender = forms.EmailField(required=True, label="Email",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Your Email Address"}))
	subject = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"What is your concern?"}))
	message = forms.CharField(required=True,widget=forms.Textarea(attrs={'class': 'form-control','placeholder':"Your message here"}))
	cc_myself = forms.BooleanField(label="Would you like to be cc'ed on the email?",required=False)


class ForgotForm(forms.Form):
	email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"The email you registered with"}))


class DonateForm(forms.Form):
	amount = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
	
	def make_payment(request):
		print request
		# try:
		# 	project = Project.objects.get(id=project_id)
		# except Project.DoesNotExist:
		# 	return False
		print project


class AddForm(forms.Form):
	project_name = forms.CharField(max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Project Name"}))
	description = forms.CharField(required=True,widget=forms.Textarea(attrs={'class': 'form-control','placeholder':"Your project description."}))
	target_money = forms.IntegerField(required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"e.g. 10000"}))
	image = forms.ImageField(required=True,help_text="Images are required. Upload an image of the concept or the wireframes of your project, and bring it to life!",widget=forms.FileInput(attrs={'class': 'form-control','placeholder':"e.g. 10000"}))
	
class EditForm(forms.Form):
	project_name = forms.CharField(max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Project Name"}))
	description = forms.CharField(required=True,widget=forms.Textarea(attrs={'class': 'form-control','placeholder':"Your project description."}))
	
	def update(self,d):
		project = d['project']
		project.name = self.cleaned_data['project_name']
		project.description = self.cleaned_data['description']
		project.save()


class UserCreateForm(UserCreationForm):
	name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'FirstName LastName'}))
	email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Please enter a valid email address so we can reach you.'}))
	a = forms.BooleanField(label="Python, Django",required=False)
	b = forms.BooleanField(label="Java, Javascript",required=False)
	c = forms.BooleanField(label="C, C++, C#", required=False)
	d = forms.BooleanField(label="Ruby, Ruby on Rails",required=False)
	e = forms.BooleanField(label="HTML, CSS",required=False)
	f = forms.BooleanField(label="PHP",required=False)
	g = forms.BooleanField(label="Perl",required=False)
	h = forms.BooleanField(label="ASP & VBScript", required=False)
	i = forms.BooleanField(label="Adobe Photoshop, Illustrator",required=False)
	j = forms.BooleanField(label="SQL Databases",required=False)
	
	username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Your username (Only letters and numbers, no spaces allowed)'}))
	password1 = forms.CharField(label="Password", max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'For your security, we will never store your password as text.'}))
	password2 = forms.CharField(label="Password Confirmation", max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password Confirmation'}))
	
	image = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))
	
	class Meta:
		model = User
		fields = ("name","username","password1","password2","email")
		
	def save(self, commit=True,image=None):
		user = super(UserCreateForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		fullName = self.cleaned_data["name"]
		a = self.cleaned_data["a"]
		b = self.cleaned_data["b"]
		c = self.cleaned_data["c"]
		d = self.cleaned_data["d"]
		e = self.cleaned_data["e"]
		f = self.cleaned_data["f"]
		g = self.cleaned_data["g"]
		h = self.cleaned_data["h"]
		i = self.cleaned_data["i"]
		j = self.cleaned_data["j"]
		A = Skill.objects.get(id=1)
		B = Skill.objects.get(id=2)
		C = Skill.objects.get(id=3)
		D = Skill.objects.get(id=4)
		E = Skill.objects.get(id=5)
		F = Skill.objects.get(id=6)
		G = Skill.objects.get(id=7)
		H = Skill.objects.get(id=8)
		I = Skill.objects.get(id=9)
		J = Skill.objects.get(id=10)
		
		if commit and image:
			user.save()
			userProfile = UserProfile(user=user, name=fullName,image=image,mimetype=image.content_type)
			
			userProfile.save()
			if a: userProfile.skill.add(A)
			if b: userProfile.skill.add(B)
			if c: userProfile.skill.add(C)
			if d: userProfile.skill.add(D)
			if e: userProfile.skill.add(E)
			if f: userProfile.skill.add(F)
			if g: userProfile.skill.add(G)
			if h: userProfile.skill.add(H)
			if i: userProfile.skill.add(I)
			if j: userProfile.skill.add(J)
		return user


class UserUpdateForm(forms.Form):
	name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'FirstName LastName'}))
	email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Please enter a valid email address so we can reach you. No spam. Ever.'}))
	
	password1 = forms.CharField(label="Old Password",widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter your password to save the changes.'}),required=False)
	password2 = forms.CharField(label="New Password?",widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Only enter new password if you want to change it.'}),required=False)
	password3 = forms.CharField(label="Confirm New Password",widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirm New Password'}),required=False)
	
	a = forms.BooleanField(label="Python, Django",required=False)
	b = forms.BooleanField(label="Java, Javascript",required=False)
	c = forms.BooleanField(label="C, C++, C#", required=False)
	d = forms.BooleanField(label="Ruby, Ruby on Rails",required=False)
	e = forms.BooleanField(label="HTML, CSS",required=False)
	f = forms.BooleanField(label="PHP",required=False)
	g = forms.BooleanField(label="Perl",required=False)
	h = forms.BooleanField(label="ASP & VBScript", required=False)
	i = forms.BooleanField(label="Adobe Photoshop, Illustrator",required=False)
	j = forms.BooleanField(label="SQL Databases",required=False)
	
	class Meta:
		fields = ("name","username","password1","password2","email")
		
	def update(self,d):
		u = d['user']
		up = d['user_profile']
		if (self.cleaned_data['password1'] != ""): # old password is not empty
			if u.check_password(self.cleaned_data['password1']):
				u.email = self.cleaned_data['email']
				up.name = self.cleaned_data['name']
				if (self.cleaned_data['password2'] != "") and (self.cleaned_data['password2'] == self.cleaned_data['password3']):
					u.set_password(self.cleaned_data['password2'])
				u.save()
				up.save()
			else: #password is incorrect
				pass
		else: #password is empty
			pass
		a = self.cleaned_data["a"]
		b = self.cleaned_data["b"]
		c = self.cleaned_data["c"]
		d = self.cleaned_data["d"]
		e = self.cleaned_data["e"]
		f = self.cleaned_data["f"]
		g = self.cleaned_data["g"]
		h = self.cleaned_data["h"]
		i = self.cleaned_data["i"]
		j = self.cleaned_data["j"]
		A = Skill.objects.get(id=1)
		B = Skill.objects.get(id=2)
		C = Skill.objects.get(id=3)
		D = Skill.objects.get(id=4)
		E = Skill.objects.get(id=5)
		F = Skill.objects.get(id=6)
		G = Skill.objects.get(id=7)
		H = Skill.objects.get(id=8)
		I = Skill.objects.get(id=9)
		J = Skill.objects.get(id=10)
		if a: up.skill.add(A)
		else: up.skill.remove(A)
		if b: up.skill.add(B)
		else: up.skill.remove(B)
		if c: up.skill.add(C)
		else: up.skill.remove(C)
		if d: up.skill.add(D)
		else: up.skill.remove(D)
		if e: up.skill.add(E)
		else: up.skill.remove(E)
		if f: up.skill.add(F)
		else: up.skill.remove(F)
		if g: up.skill.add(G)
		else: up.skill.remove(G)
		if h: up.skill.add(H)
		else: up.skill.remove(H)
		if i: up.skill.add(I)
		else: up.skill.remove(I)
		if j: up.skill.add(J)
		else: up.skill.remove(J)


class CompanyCreateForm(UserCreationForm):
	name = forms.CharField(max_length=200,help_text="Company's Name", widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Company's Email"}))
	email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Company's Email"}))
	image = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))
	
	username = forms.CharField(max_length=200, help_text="Company's Name", widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Company's Username"}))
	password1 = forms.CharField(label="Password",max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'For your security, we will never store your password as text.'}))
	password2 = forms.CharField(label="Password Confirmation",max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password Confirmation'}))
	
	class Meta:
		model = User
		fields = ("name","username","password1","password2","email")
		
	def save(self, commit=True, image=None):
		user = super(CompanyCreateForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		fullName = self.cleaned_data["name"]
		
		if commit and image:
			user.save()
			userProfile = UserProfile(user=user, name=fullName,is_company=True,image=image,mimetype=image.content_type)
			userProfile.save()
		return user

class CompanyUpdateForm(forms.Form):	
	name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'FirstName LastName'}))
	email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Please enter a valid email address so we can reach you. No spam. Ever.'}))
	password1 = forms.CharField(label="Old Password",widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter your password to save the changes.'}),required=False)
	password2 = forms.CharField(label="New Password?",widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Only enter new password if you want to change it.'}),required=False)
	password3 = forms.CharField(label="Confirm New Password",widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirm New Password'}),required=False)
	
	class Meta:
		fields = ("name","email","password1","password2",'password3')
	
	def update(self,d):
		if (self.cleaned_data['password1'] != ""): # old password is not empty
			u = d['user']
			if u.check_password(self.cleaned_data['password1']):
				up = d['user_profile']
				u.email = self.cleaned_data['email']
				up.name = self.cleaned_data['name']
				if (self.cleaned_data['password2'] != "") and (self.cleaned_data['password2'] == self.cleaned_data['password3']):
					u.set_password(self.cleaned_data['password2'])
				u.save()
				up.save()
			else: #password is incorrect
				pass
		else: #password is empty
			pass