from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


app_name = 'pollingSite'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.account_login, name='login'),
    path('search', views.search, name='search'),
    path('<str:classroom>', views.classroom, name='classroom'),
    path('<str:classroom>/attendance', views.attendance, name='attendance'),
    path('<str:classroom>/createPoll/', views.createPoll, name='createPoll'),
    path('<str:classroom>/<int:poll>/active', views.activePoll, name='activePoll'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)