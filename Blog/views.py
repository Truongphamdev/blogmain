from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import Post,Author
from .form import FormComment,PostForm
from django.views.generic import ListView
from django.views import View
from django.urls import reverse
from django.utils.text import slugify
# Create your views here.
class StartPage(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'posts'
    def get_queryset(self):
        query = super().get_queryset()
        data = query[:3]
        return data

# def start_page(request):
#     latest_posts = Post.objects.all().order_by('-date')[:3]
#     return render(request,'blog/index.html', {
#         "posts":latest_posts
#     })
class Posts(ListView):
    template_name = 'blog/all-posts.html'
    model = Post
    context_object_name = 'all_posts'
    ordering = ['-date']
# def posts(request):
#     return render(request,'blog/all-posts.html',{
#         "all_posts":Post.objects.all().order_by('-date')
#     })
class PostDetail(View):
    def stored(self,request,post_id):
        stored_posts = request.session.get('stored_post')
        if stored_posts is not None:
            is_saving_later = post_id in stored_posts
        else:
            is_saving_later = False
        return is_saving_later
    def get(self,request,slug):
        post = Post.objects.get(slug=slug)
        
        context = {
            'post':post,
            'post_tags':post.tags.all(),
            'comments':FormComment(),
            'comment_value':post.comments.all().order_by('-id'),
            'saving_later':self.stored(request,post.id)
        }
        return render(request,'blog/post-detail.html',context)
    def post(self,request,slug):
        comment_form = FormComment(request.POST)
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post-detail-page',args=[slug]))
        context = {
            'post':post,
            'post_tags':post.tags.all(),
            'comments':FormComment(),
            'comment_value':post.comments.all().order_by('-id'),
            'saving_later':self.stored(request,post.id)


        }
        return render(request,'blog/post-detail.html',context)
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['post_tags'] = self.object.tags.all()
    #     context['comments'] = FormComment()
    #     return context
# def post_detail(request,slug):
#     post_curent = get_object_or_404(Post,slug = slug)
#     return render(request,"blog/post-detail.html",{
#         "post":post_curent,
#         "post_tags":post_curent.tags.all()
#     })
class ReadLater(View):
    def get(self,request):
        stored_post = request.session.get('stored_post')
        context = {}
        if stored_post is None or len(stored_post)==0:
            context['posts'] = []
            context['has_posts'] = False
        else:
            posts = Post.objects.filter(id__in = stored_post)
            context['posts'] = posts
            context['has_posts'] = True
        return render(request,'blog/store_post.html',context)
    def post(self,request):
        stored_post = request.session.get('stored_post')
        if stored_post is None:
            stored_post = []
        post_id = int(request.POST['post_id'])
        if post_id not in stored_post:
            stored_post.append(post_id)
        else:
            stored_post.remove(post_id)
        request.session['stored_post'] = stored_post
        return HttpResponseRedirect('/')
class AddPost(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'blog/addpost.html', {
            'forms': form
        })

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # Lấy dữ liệu từ form
            author_first_name = form.cleaned_data['author_first_name']
            author_last_name = form.cleaned_data['author_last_name']
            author_email = form.cleaned_data['author_email']

            # Tạo hoặc lấy tác giả
            author, created = Author.objects.get_or_create(
                first_name=author_first_name,
                last_name=author_last_name,
                email_address=author_email
            )

            # Tạo bài viết
            post = form.save(commit=False)
            post.author = author
            post.slug = slugify(form.cleaned_data['title'])  # Tạo slug từ tiêu đề
            post.save()
            form.save_m2m() 
            # Điều hướng đến trang chi tiết bài viết
            return redirect('post-detail-page', slug=post.slug)  # Chuyển hướng đến trang chi tiết bài viết
        else:
            # Nếu form không hợp lệ, render lại template với lỗi
            return render(request, 'blog/addpost.html', {
                'forms': form
            })