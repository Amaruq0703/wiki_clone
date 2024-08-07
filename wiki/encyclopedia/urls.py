from django.urls import path

from . import views

app_name = 'encyclopedia'

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>', views.getentry, name = 'getentry'),
    path("search", views.search, name="search"),
    path("create", views.createentry, name='create'),
    path("wiki/edit/<str:title>", views.editpage, name="edit"),
    path('random', views.randompage, name='random')
]
