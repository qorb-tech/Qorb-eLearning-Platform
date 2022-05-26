from django.urls import path

# Local Imports Goes Here!
from .views import (
    create_question,
    create_question_form,
    delete_question,
    detail_question,
    quizzes,
    update_question,
)

urlpatterns = [
    path("current-quizzes/", quizzes, name="quizzes"),
    path("<pk>/", create_question, name="create_question"),
    path("htmx/question/<pk>/", detail_question, name="detail_question"),
    path("htmx/question/<pk>/update/", update_question, name="update_question"),
    path("htmx/question/<pk>/delete/", delete_question, name="delete_question"),
    path(
        "htmx/create-question-form/", create_question_form, name="create_question_form"
    ),
]
