''' This will be the URL Dispatcher, i.e., the file that will be in charge of
linking the pages to the controller '''

from django.conf.urls import patterns, url
from django.contrib.auth import authenticate, login
from yalladevelop import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^signup/$', views.signup_user, name="signup"),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'yalladevelop/login.html'}, name="login"),
	url(r'^logout/$', views.logout_user, name="logout"),
	url(r'^project/(?P<project_id>\d+)/$', views.showProject, name='showProject'),
	url(r'^profile/(?P<profile_id>\d+)/$', views.showProfile, name='showProfile'),
	url(r'^profile/$', views.showProfile, name='showProfile'),
	url(r'^addproject/$', views.addProject, name='addProject'),
	url(r'^forgotpassword/$', views.forgotPassword, name='forgotPassword'),
	url(r'^profile_settings/$', views.profileSettings, name='profileSettings'),
	
	url(r'^userorcompany/$', views.userorcompany, name="userorcompany"),
	url(r'^user-signup/$', views.signup_user, name="signup_user"),
	url(r'^track/$', views.track, name="track"),
	url(r'^company-signup/$', views.signup_company, name="signup_company"),	
	
	url(r'^search_skills/$', views.search_skills, name="search_skills"),	
	url(r'^search_skills/(?P<skill_id>\d+)/$', views.search_skills, name="search_skills"),	
	
	# Functions dispatcher
	url(r'^project/(?P<project_id>\d+)/likeProject$', views.likeProject, name='likeProject'),
	url(r'^project/(?P<project_id>\d+)/helpProject$', views.helpProject, name='helpProject'),
	url(r'^project/(?P<project_id>\d+)/donate/$', views.donate, name='donate'),
	
	url(r'^project/(?P<project_id>\d+)/edit$', views.editProject, name='editProject'),
	
	url(r'^post_comment/$', views.postComment, name='postComment'),
	
	url(r'^user_upload/$', views.user_upload, name='user_upload'),
	
	# Static Pages Dispatcher
	url(r'^about/$', views.about, name="about"),
	url(r'^contact/$', views.contact, name="contact"),
	url(r'^explore/$', views.explore, name="explore"),
	url(r'^allprojects/$', views.allprojects, name="allprojects"),
	url(r'^allusers/$', views.allusers, name="allusers"),
	url(r'^allcompanies/$', views.allcompanies, name="allcompanies"),
	url(r'^faq/$', views.faq, name="faq"),
	url(r'^help/$', views.help, name="help"),
	url(r'^privacy/$', views.privacy, name="privacy"),
	url(r'^sitemap/$', views.sitemap, name="sitemap"),
	url(r'^terms/$', views.terms, name="terms"),
	url(r'^rankings/$', views.rankings, name='rankings'),
	
	url(r'^getProfilePicture/ (?P<user_id>\d+)/$', views.getProfilePicture, name='getProfilePicture'),
	url(r'^getProjectPicture/ (?P<project_id>\d+)/$', views.getProjectPicture, name='getProjectPicture'),
		
	# DEVELOEPR HELP
	url(r'^developerhelp/$', views.dhelp, name='dhelp'),
)