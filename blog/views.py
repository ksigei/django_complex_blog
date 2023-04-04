from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Bookmark, Vote
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.shortcuts import redirect, get_object_or_404


def home(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'home.html', {'posts': posts})


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)

    # comment form
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    # # bookmark
    # if request.user.is_authenticated:
    #     if request.user in post.bookmarks.all():
    #         context['bookmark'] = True
    #     else:
    #         context['bookmark'] = False

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }


    return render(request, 'post_detail.html', context)


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(is_published=False).order_by('published_date')
    return render(request, 'post_draft_list.html', {'posts': posts})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.is_published = True
    post.published_date = timezone.now()
    post.save()
    return redirect('post_draft_list')


def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('home')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'form': form})


def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


def vote(request, pk, vote_type):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    vote, created = Vote.objects.get_or_create(post=post, author=user, defaults={'vote_type': vote_type})
    if not created:
        vote.vote_type = vote_type
        vote.save()
    return redirect('post_detail', pk=post.pk)


def bookmark(request, pk):
    post = get_object_or_404(Post, pk=pk)
    bookmark = Bookmark.objects.create(post=post, author=request.user)
    bookmark.save()
    return redirect('post_detail', pk=post.pk)


@login_required
def bookmarks(request):
    bookmarks = Bookmark.objects.filter(author=request.user)
    return render(request, 'bookmarks.html', {'bookmarks': bookmarks})


def unbookmark(request, pk):
    bookmark = get_object_or_404(Bookmark, pk=pk)
    bookmark.delete()
    return redirect('bookmarks')

def uncomment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
