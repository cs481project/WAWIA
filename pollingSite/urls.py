from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.urls import views as auth_views
from . import views


app_name = 'pollingSite'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('', auth_views.LoginView.as_view(template_name='pollingSite/login.html'), name='login'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='pollingSite/changePassword.html'), name='changePassword'),
    path('search/', views.search, name='search'),
    path('addclass/', views.addClass, name='addClass'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('<str:classroom>/', views.classroom, name='classroom'),
    path('<str:classroom>/attendance/', views.attendance, name='attendance'),
    path('<str:classroom>/attendanceform/', views.attendanceForm, name='attendanceForm'),
    path('<str:classroom>/polllist/', views.pollList, name='pollList'),
    path('<str:classroom>/createpoll/', views.createPoll, name='createPoll'),
    path('<str:classroom>/<int:poll>/active/', views.activePoll, name='activePoll'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)