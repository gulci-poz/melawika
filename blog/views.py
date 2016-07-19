from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView


class PostListView(ListView):
    # równie dobrze możemy podać model = Post i django zbuduje QuerySet
    queryset = Post.published.all()
    # domyślnym obiektem jest object_list
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request):
    object_list = Post.published.all()
    # 3 posty na każdą stronę
    paginator = Paginator(object_list, 3)
    # parametr GET zawiera numer bieżącej strony
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # pierwsza strona, jeśli page nie jest liczbą całkowitą
        posts = paginator.page(1)
    except EmptyPage:
        # ostatnia strona rezultatów, jeśli page jest out of range
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
