from django.urls import path

from task_manager.statuses import views

urlpatterns = [
    path("", views.StatusesList.as_view(), name='statuses'),
    path("create/", views.StatusCreationView.as_view(), name='status_create'),
]
