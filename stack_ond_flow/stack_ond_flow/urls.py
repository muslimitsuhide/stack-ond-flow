"""
URL configuration for stack_ond_flow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from askme import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls, name='admin'),
    path('question/<int:question_id>', views.question, name='question'),
    path('question/<int:question_id>/page/<int:page_num>', views.question, name='question_page'),
    path('login/', views.login, name='login'),
    path('singup/', views.register, name='register'),
    path('hot/', views.index, name='index'),
    path('ask/', views.ask, name='ask'),
    path('tag/<str:tag>/', views.tag, name='tag'),
    path('tag/<str:tag>/page/<int:page_num>', views.tag, name='tag_page')
]
