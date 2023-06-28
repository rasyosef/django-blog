from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.


class BlogListView(ListView):
    model = Post
    template_name = "home.html"


class BlogDetailVeiw(DetailView):
    model = Post
    template_name = "post_detail.html"
