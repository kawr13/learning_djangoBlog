from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from blogapp.models import Post, Comments
from django.views.generic import ListView
from blogapp.forms import EmailPostForm, CommentForm, SearchForm
from icecream import ic
from django.core.mail import send_mail
from blogproject.settings import EMAIL_HOST_USER
from django import forms
from blogapp.multitask import multipool
from taggit.models import Tag
from django.db.models import Count
import time

# Create your views here.


lst_num = 0  # Используем глобальную переменную для счетчика


@multipool
def cycle():
    global lst_num
    while True:
        lst_num += 1
        time.sleep(10)


# cycle()
class PostSearchView(View):

    def get(self, request):
        form = SearchForm()
        query = None
        result = []
        if 'query' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']
                search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
                search_query = SearchQuery(query)
                result = Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)
                                                 ).filter(rank__gte=0.3).order_by('-rank')

        context = {
            'title': 'Search',
            'form': form,
            'query': query,
            'results': result
        }
        return render(request, 'blogapp/blog_search.html', context=context)

class BlogListView(View):

    def get(self, request, tag_slug=None):
        posts_lists = Post.published.all()
        tag = None
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            posts_lists = posts_lists.filter(tags__in=(tag,))

        paginator = Paginator(posts_lists, 3)
        page_number = request.GET.get('page', 1)
        try:
            posts = paginator.page(page_number)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context = {
            'title': 'Blog',
            'posts': posts,
        }
        return render(request, 'blogapp/blog.html', context=context)

    # template_name = 'blogapp/blog.html'
    # queryset = Post.published.all()
    # context_object_name = 'posts'
    # paginate_by = 3
    # tag_slug = None
    # tag = None
    #
    # def get_queryset(self, **kwargs):
    #     queryset = super().get_queryset(**kwargs)
    #     tag_slug = self.kwargs.get('tag_slug')
    #     if tag_slug:
    #         tag = get_object_or_404(Tag, slug=tag_slug)
    #         queryset = queryset.filter(tags__in=[tag])
    #     return queryset
    #
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Blog'
    #     context['lst_num'] = lst_num
    #     context['tag'] = self.tag_slug
    #
    #     return context




class PostDetailView(View):

    def get(self, request, year, month, day, slug):
        form = EmailPostForm()
        comments_form = CommentForm()
        post = Post.published.get(
            publish__year=year,
            publish__month=month,
            publish__day=day,
            slug=slug
        )
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
        comments = Comments.objects.filter(post=post, active=True).select_related('post')
        if comments:
            email_choices = [(comment.email, comment.email) for comment in comments]
            form.fields['to'] = forms.ChoiceField(choices=email_choices)
        context = {
            'title': post.title,
            'post': post,
            'form': form,
            'comments': comments,
            'commentsform': comments_form,
            'similar_posts': similar_posts,
        }
        return render(request, 'blogapp/blog_detailed.html', context=context)

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        form = EmailPostForm(request.POST)
        sent = False
        comments_form = CommentForm(request.POST)

        if form.is_valid():

            to = request.POST.get('to', '')
            name = form.cleaned_data['name']
            ic(to)
            comments = form.cleaned_data['comments']
            send_mail(
                subject=f'{name} оставил комментарии к посту {post.title}',
                message=f'{post.body}\nКомментарий:\n{comments}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[to],
            )
            return HttpResponseRedirect(post.get_absolute_url())
        elif comments_form.is_valid():
            ic(comments_form)
            comment = comments_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
        else:
            return HttpResponseRedirect(post.get_absolute_url())
