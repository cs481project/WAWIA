from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


app_name = 'pollingSite'
urlpatterns = [#				URL\/
    path('', views.landing, name='landing'),
    path('index', views.index, name='index'),
    path('login', views.login, name='login'),
    path('change-password', views.changePassword, name='changePassword'),
    path('search', views.search, name='search'),
    path('addclass', views.addClass, name='addClass'),
    path('<str:classroom>/', views.classroom, name='classroom'),
    path('<str:classroom>/attendance/', views.attendance, name='attendance'),
    path('<str:classroom>/polllist/', views.pollList, name='pollList'),
    path('<str:classroom>/createpoll/', views.createPoll, name='createPoll'),
    path('<str:classroom>/<int:poll>/active/', views.activePoll, name='activePoll'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)