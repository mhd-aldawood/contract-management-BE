# educational_contents/urls.py
from django.urls import path
from .views import (
    EducationalContentListCreateView,
    EducationalContentDetailView,
    EducationalContentUploadView,
)

urlpatterns = [
    path("educational-contents", EducationalContentListCreateView.as_view(), name="edu-list-create"),
    path("educational-contents/<int:pk>/", EducationalContentDetailView.as_view(), name="edu-detail"),
    path("educational-contents/upload/", EducationalContentUploadView.as_view(), name="edu-upload"),
]