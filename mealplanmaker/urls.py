
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("mealcreation", views.mealcreation, name="mealcreation"),
    path("weekly", views.weekly, name="weekly"),
    path("deletemeal", views.deletemeal, name="deletemeal"),
    path("deletefromplan", views.deletefromplan, name="deletefromplan"),
    path("find_recipes/", views.find_recipes, name='find_recipes'),
    path("shelf/", views.shelf, name='shelf')
    
]

