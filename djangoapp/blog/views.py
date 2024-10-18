from typing import Any
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Page
from django.db.models import Q, QuerySet
from django.views.generic import ListView

PER_PAGE = 9


class PostListView(ListView):
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(is_published=True)
    #     return queryset

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Home - ',

        })
        return context


# def index(request):
#     posts = Post.objects.get_published()
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             # 'page_title': 'Home - ',
#         }
#     )

class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username

        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        page_title = user_full_name + " - Posts "

        ctx.update({
            'page_title': page_title,
        })

        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)
        return qs

    def get(self, request, *args, **kwargs):
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404()

        self._temp_context.update({
            'author_pk': author_pk,
            'user': user,
        })

        return super().get(request, *args, **kwargs)


# def created_by(request, author_pk):
#     user = User.objects.filter(pk=author_pk).first()
#     if user is None:
#         raise Http404()  # Levanta 404 se o usuário não for encontrado

#     # Obtém os posts do usuário
#     posts = Post.objects.get_published().filter(created_by__pk=author_pk)

#     # Lógica para montar o nome completo do usuário
#     if user.first_name and user.last_name:
#         user_full_name = f'{user.first_name} {user.last_name}'
#     elif user.first_name:
#         user_full_name = user.first_name
#     else:
#         user_full_name = user.username

#     page_title = f'{user_full_name} Posts - '

#     # Paginação
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )

class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = (
            f'{self.object_list[0].category.name}'  # type: ignore
            ' - Categoria - '
        )
        ctx.update({
            'page_title': page_title,
        })
        return ctx


# def category(request, slug):
#     posts = Post.objects.get_published().filter(category__slug=slug)
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     if len(page_obj) == 0:
#         raise Http404()

#     page_title = f'{page_obj[0].category.name} - '

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,

#         }
#     )

class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = (
            f'{self.object_list[0].tags.first().name}'  # type: ignore
            ' - Tag - '
        )
        ctx.update({
            'page_title': page_title,
        })
        return ctx


# def tag(request, slug):
#     # Filtra os posts pela tag
#     posts = Post.objects.get_published().filter(tags__slug=slug)

#     # Levanta 404 se não houver posts
#     if not posts.exists():
#         raise Http404("No posts found for this tag.")

#     # Paginação
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     # Define o título da página usando a tag do primeiro post
#     first_post_tag = page_obj[0].tags.first()
#     page_title = f'{first_post_tag.name} - ' if first_post_tag else 'Tag - '

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )

class SearchListView(PostListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search_value = ''

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        search_value = self._search_value
        return super().get_queryset().filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[:PER_PAGE]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        search_value = self._search_value
        ctx.update({
            'page_title': f'{search_value[:30]} - Search - ',
            'search_value': search_value,
        })
        return ctx

    def get(self, request, *args, **kwargs):
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)


# def search(request):
#     search_value = request.GET.get('search', '').strip()

#     # Verifica se o search_value não está vazio
#     if search_value:
#         posts = (Post.objects.get_published()
#                  .filter(
#                      Q(title__icontains=search_value) |
#                      Q(excerpt__icontains=search_value) |
#                      Q(content__icontains=search_value)
#         ))
#     else:
#         posts = Post.objects.none()  # Retorna uma QuerySet vazia se não houver valor de busca

#     # Definindo o título da página
#     page_title = f'Search results for: {search_value[:30]} - ' if search_value else 'Search - '

#     # Paginação
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,  # Passa o objeto paginado
#             'search_value': search_value,
#             'page_title': page_title,
#         }
#     )


def page(request, slug):
    # Tenta obter a página correspondente ao slug. Se não existir, retorna 404.
    page_obj = get_object_or_404(Page, is_published=True, slug=slug)

    # Define o título da página com o título da página
    page_title = f'{page_obj.title} - '  # Personalize conforme necessário

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page_obj,
            'show_description': False,
            'page_title': page_title,  # Adiciona o título da página ao contexto
        }
    )


def post(request, slug):
    # Tenta obter o post correspondente ao slug. Se não existir, retorna 404.
    post_obj = get_object_or_404(Post.objects.get_published(), slug=slug)

    # Se o modelo Post tiver uma relação ManyToMany com Tag
    tags = post_obj.tags.all()  # Isso obtém todas as tags associadas ao post

    # Define o título da página com o título do post
    page_title = f'{post_obj.title} - '

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            'tags': tags,
            'page_title': page_title,  # Adiciona o título da página ao contexto
        }
    )
