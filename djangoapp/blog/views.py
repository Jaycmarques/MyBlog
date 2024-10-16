from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Post
from django.db.models import Q

PER_PAGE = 9


def index(request):
    posts = Post.objects.get_published()
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def created_by(request, author_pk):
    posts = Post.objects.get_published().filter(created_by__pk=author_pk)
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def category(request, slug):
    posts = Post.objects.get_published().filter(category__slug=slug)
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def tag(request, slug):
    posts = Post.objects.get_published().filter(tag__slug=slug)
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def search(request):
    search_value = request.GET.get('search', '').strip()
    posts = (Post.objects.get_published()
             .filter(
                 Q(title__icontains=search_value) |
                 Q(excerpt__icontains=search_value) |
                 Q(content__icontains=search_value)
    )
    )
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
        }
    )


def page(request, slug):

    return render(
        request,
        'blog/pages/page.html',
        {
            # 'page_obj': page_obj,
        }
    )


def post(request, slug):
    post = Post.objects.get_published().filter(slug=slug).first()

    # Defina suas tags aqui
    tags = ["Testando", "Atenção", "Obrigado", "Educação", "Python"]

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post,
            'tags': tags,  # Adiciona as tags ao contexto
        }
    )
