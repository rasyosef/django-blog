from django.urls import path
from .views import BlogListView, BlogDetailVeiw

urlpatterns = [
    path("", BlogListView.as_view(), name="home"),
    path("post/<int:pk>/", BlogDetailVeiw.as_view(), name="post_detail"),
]
