from django.shortcuts import render, get_object_or_404, redirect
# from django.urls import reverse
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


@login_required
def LikeView(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, id=request.POST.get('post_id'))
        liked = False
        PostListView.liked = False
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        context = {
            'post': post,
            'is_liked': liked,
        }
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'), context)
    else:
        return redirect('blog-home')


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    # <app>/<model>_<viewtype>.html

    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        print(self.kwargs)
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        liked = False
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['total_likes'] = stuff.total_likes()
        context['liked'] = liked
        context['kwargs'] = self.kwargs
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

def about(request):

    return render(request, 'blog/about.html', {'title': 'About'})
