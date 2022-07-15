from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("create", views.create, name="create"),
    path("random", views.haphazard, name="random"),
    path("search", views.search, name="search"),
    path("error/<str:message>", views.error, name="error")


]
