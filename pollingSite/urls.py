from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.urls import views as auth_views
from . import views


app_name = 'pollingSite'
urlpatterns = [
    path('', views.landing, name='landing'),
    path('index/', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='pollingSite/login.html'), name='login'),
    path('change-password/password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='pollingSite/changePasswordComplete.html'), name='password_change_done'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='pollingSite/changePassword.html', success_url='password_change_done/'), name='changePassword'),
	path('receive_sms/', views.recieveSMS, name='sms'),
    path('addclass/', views.addClass, name='addClass'),
    path('report/', views.report, name='report'),
    path('poll/', views.pollLanding, name='pollLanding'),
    path('editclass/<int:classroom>/', views.edit, name='edit'),
    path('setActive/<int:classroom>/', views.setActive, name='setActive'),
    path('poll/<str:classroom>/createpoll/', views.createPoll, name='createPoll'),
    path('poll/<str:classroom>/<int:poll>/active/', views.activePoll, name='activePoll'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)