from django.urls import path

from . import views

urlpatterns = [
    # url: /attendance/
    path("", views.index, name="index"),
    # url: /attendance/class5/
    path("class<int:class_id>/", views.detail, name="detail"),
]
