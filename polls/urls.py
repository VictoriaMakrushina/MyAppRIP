from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#from django.core.urlresolvers import reverse
from django.urls import reverse


urlpatterns = [
    url(r'^$', views.CoursesView.as_view(), name='start'),
    url(r'^polls/$',views.polls,name='polls'),
    url(r'^course/(?P<id>\d+)/$', views.CourseView.as_view(), name='course_detail'),
    url(r'^course/$',views.CoursesView.as_view(),name='course'),
    url(r'^authen/',views.Authen.as_view(),name='authen'),
    url(r'^reg/$',views.reg,name='reg'),
    url(r'^teachers/$', views.UsersView.as_view(), name='teacher'),
	url(r'^teacher/(?P<id>\d+)/$', views.UserView.as_view(), name='repet-detail'),
    url(
	   r'^teacher/(?P<id>\d+)/follows/(?P<fid>\d+)$',
	   views.user_cooperate,
	   name='user_cpr'),
	url(
	   r'^teacher/(?P<id>\d+)/unfollows/(?P<fid>\d+)$',
	   views.user_uncooperate,
	   name='user_ucpr'),
	url(r'^login/', views.authorization, name='login'),
	url(r'^logout/', views.exit, name='logout'),
    url(r'^thanks/$',views.thanks,name='thanks'),
    url(r'^newcourse/$',views.newcourse,name='newcourse'),
    url(r'^load/', views.LoadView.as_view()),
#url(r'^register/$', views.register, name='register'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()