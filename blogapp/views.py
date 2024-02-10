from django.shortcuts import render
from django.views import View
from blogapp.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

# Create your views here.

class BlogListView(ListView):
    template_name = 'blogapp/blog.html'

    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3


    # def get(self, request):
    #     posts_lists = Post.published.all()
    #     paginator = Paginator(posts_lists, 1)
    #     page_number = request.GET.get('page', 1)
    #     try:
    #         posts = paginator.page(page_number)
    #     except PageNotAnInteger:
    #         posts = paginator.page(1)
    #     except EmptyPage:
    #         posts = paginator.page(paginator.num_pages)
    #     context = {
    #         'title': 'Blog',
    #         'posts': posts,
    #     }
    #     return render(request, self.template_name, context=context)


class PostDetailView(View):
    template_name = 'blogapp/blog_detailed.html'

    def get(self, request, year, month, day, slug):
        post = Post.published.get(
            publish__year=year,
            publish__month=month,
            publish__day=day,
            slug=slug
        )
        context = {
            'title': post.title,
            'post': post
        }
        return render(request, self.template_name, context=context)