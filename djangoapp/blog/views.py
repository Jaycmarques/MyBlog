from django.core.paginator import Paginator
from django.shortcuts import render

posts = list(range(1000))


def index(request):
    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def page(request):
    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/page.html',
        {
            # 'page_obj': page_obj,
        }
    )


def post(request):
    # Supondo que posts esteja definido em algum lugar do seu código
    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Defina suas tags aqui
    tags = ["Testando", "Atenção", "Obrigado", "Educação", "Python"]

    return render(
        request,
        'blog/pages/post.html',
        {
            'page_obj': page_obj,
            'tags': tags,  # Adiciona as tags ao contexto
        }
    )
