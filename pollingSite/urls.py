from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.urls import views as auth_views
from . import views


app_name = 'pollingSite'
urlpatterns = [
    path('', views.landing, name='landing'),
    path('index/', views.index, name='index'),
    path('class/', views.addSearchClass, name='addSearchClass'),
    path('login/', auth_views.LoginView.as_view(template_name='pollingSite/login.html'), name='login'),
    path('settings/usersettings/', views.settings, name='settings'),
    path('settings/change-password/password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='pollingSite/changePasswordComplete.html'), name='password_change_done'),
    path('settings/change-password/', auth_views.PasswordChangeView.as_view(template_name='pollingSite/changePassword.html', success_url='password_change_done/'), name='changePassword'),
	path('receive_sms/', views.recieveSMS, name='sms'),
    path('addclass/', views.addClass, name='addClass'),
    path('report/', views.report, name='report'),
    path('poll/', views.pollLanding, name='pollLanding'),
    path('info/<str:classroom>/', views.info, name='info'),
    path('setActive/<int:classroom>/', views.setActive, name='setActive'),
    path('poll/<str:classroom>/createpoll/', views.createPoll, name='createPoll'),
    path('poll/<str:classroom>/<int:poll>/active/', views.activePoll, name='activePoll'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)