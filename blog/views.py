from django.shortcuts import render, redirect, get_object_or_404

from .forms import NewPostForm, NewCommentForm
from gallary.forms import BlogImageNewForm, CommentImageNewForm

from .models import Blog
from gallary.models import BlogImage, CommentImage


def blog_info(request, pk):
    context = {
        'blog': get_object_or_404(Blog, pk=pk),
        'comment_form': NewCommentForm(),
        'image_comment_form': CommentImageNewForm(),
    }
    return render(request, 'blog/blog_details.html', context)


def new_blog(request):
    if request.method == 'POST':
        blog_form = NewPostForm(request.POST)
        image_form = BlogImageNewForm(request.POST, request.FILES)
        if blog_form.is_valid() and image_form.is_valid():
            blog = blog_form.save(commit=False)
            blog.user = request.user
            blog.save()
            if request.FILES.get('image'):
                BlogImage.objects.create(
                    image=request.FILES['image'] ,
                    blog=blog,
                    user=request.user
                )
            return redirect('blog:blog_details', pk=blog.id)
    return redirect('user:home_page')


def new_comment(request, pk):
    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        image_form = CommentImageNewForm(request.POST, request.FILES)
        if comment_form.is_valid() and image_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = get_object_or_404(Blog, pk=pk)
            comment.save()
            if request.FILES.get('image'):
                CommentImage.objects.create(
                    image=request.FILES['image'],
                    comment=comment,
                    user=request.user
                )
            return redirect('blog:blog_details', pk=comment.blog.id)
    return redirect('user:home_page')
