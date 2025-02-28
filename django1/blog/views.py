from IPython.core.release import author
from django.core.handlers.wsgi import WSGIRequest
from django.forms import ModelForm, Form
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from blog.forms import PostCreateForm
from blog.models import Post, Comment


class PostListView(ListView):
    model = Post
    template_name = 'blog/posts_list_new.html'
    context_object_name = 'posts'


class CommentListView(ListView):
    model = Comment
    template_name = 'blog/comments_list_test.html'
    context_object_name = 'comments'


class PostDetailView(DetailView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/posts_detail.html'
    context_object_name = 'post'

    # def get(self, request: WSGIRequest, post_id: int):
    #
    #     my_post = Post.objects.get(id=post_id)
    #     context = {
    #         "post": my_post
    #     }
    #
    #     return render(
    #         request,
    #         template_name='blog/posts_detail.html',
    #         context=context
    #     )


class PostListViewOld(View):

    def get(self, request: WSGIRequest):

        my_posts = Post.objects.all()

        context = {
            "posts": my_posts
        }

        return render(
            request,
            template_name='blog/posts_list_new.html',
            context=context
        )


class CommentListViewOld(View):

    def get(self, request: WSGIRequest):

        my_comments = Comment.objects.all()

        context = {
            "comments": my_comments
        }

        return render(
            request,
            template_name='blog/comments_list_test.html',
            context=context
        )


def posts_list_view(request: WSGIRequest):
    """
        page = 1
        page_size = 3
        [0:3] - [(page-1)*page_size : page+page_size]
    """
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 3))

    print(f"Method: {request.method}")
    print(f"Page: {page}")

    my_posts = Post.objects.all().order_by('-created_at')[(page-1)*page_size : page*page_size]

    context = {
        "posts": my_posts,
        "current_page": page,
        "prev_page": page - 1,
        "next_page": page + 1
    }

    return render(
        request,
        template_name='blog/posts_list.html',
        context=context
    )


def posts_detail_view(request: WSGIRequest, post_id):
    print(f"Method: {request.method}")
    my_post = Post.objects.get(id=post_id)
    context = {
        "post": my_post
    }

    return render(
        request,
        template_name='blog/posts_detail.html',
        context=context
    )


def test_view(request: WSGIRequest, post_id, **kwargs):
    print("\n\n=== Starting Test View =================================")
    print(f"Request GET: {request.GET}")

    print(f"post_id: {post_id}")
    # print(f"path params: {kwargs}")

    return HttpResponse("Ok!")


class PostCreateView(CreateView):
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy('posts_list')
    template_name = 'blog/post_create_new.html'


class PostCreateViewOld(View):
    def get(self, request, *args, **kwargs):

        form = PostCreateForm()

        return render(
            request,
            template_name='blog/post_create_new.html',
            context={
                "form": form
            }
        )

    def post(self, request, *args, **kwargs):

        data = PostCreateForm(request.POST)

        if data.is_valid():
            data.save()

        return redirect('posts_list')


def post_create_view(request: WSGIRequest):
    print(f"Method: {request.method}")

    if request.method == 'GET':
        return render(
            request,
            template_name='blog/post_create.html'
        )
    elif request.method == 'POST':
        print(f"request.POST: {request.POST}")
        title = request.POST.get('title')
        content = request.POST.get('content')
        new_post = Post(
            title=title,
            content=content,
            author_id=2
        )
        new_post.save()

        return redirect('posts_list')












# response = "<h1>All Posts:</h1>"
# for post in posts:
#     response += f"<div><h4>{post.id}. {post.title}</h4>"
#     response += f"<p>{post.content}</p>"
#     response += f"<br></div>"