from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Comment, Post
from .forms import CommentForm, PostForm


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")

class PostDetail(generic.DetailView):
    queryset = Post.objects.all().order_by("-created_on")

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        request.POST._mutable = True
        request.POST["author"] = request.user
        request.POST["post"] = post
        request.POST._mutable = False

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})


class CreatePost(LoginRequiredMixin, generic.CreateView):
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("post_list")

    form_class = PostForm
    queryset = Post.objects.all()
    template_name = "blog/post_form.html"

    def post(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.POST["author"] = request.user
        request.POST._mutable = False

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PostDelete(LoginRequiredMixin, generic.DeleteView):
    queryset = Post.objects.all()
    success_url = reverse_lazy("post_list")
    


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy("login")

    queryset = Post.objects.all()
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy(
            "post_detail",
            args=(
                {
                    self.object.id,
                }
            )
        )


class PostDraftList(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy("login")
    queryset  = Post.objects.filter(status=0).order_by("-created_on")

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class PostArchivedList(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy("login")
    queryset  = Post.objects.filter(status=2).order_by("-created_on")

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)
    

@login_required
def post_publish(request, pk):
    Post.objects.filter(pk=pk).update(status=1)
    return redirect("post_detail", pk=pk)


@login_required
def post_archive(request, pk):
    Post.objects.filter(pk=pk).update(status=2)
    return redirect("post_detail", pk=pk)


@login_required
def add_comment(request, pk):
    post = Post.objects.filter(pk=pk).first()
    if request.method == "POST":
        request.POST._mutable = True
        request.POST["author"] = request.user
        request.POST["post"] = post
        request.POST._mutable = False
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = CommentForm()
    return render(request, "blog/comment_form.html", {"form": form})


@login_required
def comment_approve(request, pk):
    comment = Comment.objects.filter(pk=pk)
    post_pk = comment.first().post.pk
    comment.update(approved_comment=True)
    return redirect("post_detail", pk=post_pk)


@login_required
def comment_remove(request, pk):
    comment = Comment.objects.filter(pk=pk)
    post_pk = comment.first().post.pk
    comment.delete()
    return redirect("post_detail", pk=post_pk)


class CreateUser(generic.CreateView):
    success_url = reverse_lazy("post_list")

    form_class = UserCreationForm
    queryset = User.objects.all()
    template_name = "registration/signup.html"