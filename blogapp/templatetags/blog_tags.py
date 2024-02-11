from django import template
from django.utils.safestring import mark_safe
from blogapp.models import Post
import markdown

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.objects.count()


@register.inclusion_tag('blogapp/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.objects.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
