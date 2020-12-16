from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Post
from newsletter.models import Signup


def get_category_count():
    queryset = Post \
        .objects\
        .values('categories__title')\
        .annotate(Count('categories__title'))
    return queryset

def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

        
    context = {
        'object_list': featured,
        'latest': latest
    }
    return render(request, 'index.html' , context)
    
def blog(request):
    category_count = get_category_count()
    latest_post = Post.objects.order_by('-timestamp')[:3]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 4)
    page_request = 'page'
    page = request.GET.get(page_request)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context ={
        'queryset': paginated_queryset,
        'latest_post': latest_post,
        'page_request': page_request,
        'category_count': category_count

    }
    return render(request, 'blog.html', context )

def post(request, id):
    category_count = get_category_count()
    latest_post = Post.objects.order_by('-timestamp')[:3]
    post = get_object_or_404(Post, id=id)
    context = {
        'post': post,
        'latest_post': latest_post,
        'category_count': category_count
    }
    return render(request, 'post.html', context)