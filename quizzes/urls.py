from django.urls import path

from . import views

app_name = 'quizzes'
urlpatterns = [
    # url: /quizzes/
    path("", views.index, name="index"),
    # url: /quizzes/1/0105123
    path("<int:quiz_id>/<int:student_id>", views.detail, name="index"),
]
