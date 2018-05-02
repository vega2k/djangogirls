from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .forms import PostModelForm, PostForm,CommentForm
from .models import Post,Comment


# Create your views here
# render가 HttpResponse 객체를 생성해서 반환해준다.

def post_list(request):
    # return render(request,'blog/post_list.html',{
    #     'name':'Django','age':10
    # })     #Django Template Loader

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html',{'posts':posts})

    # return HttpResponse("""
    # <!doctype html>
    # <html>
    #     <head>
    #         <meta charset="utf-8"/>
    #         <title>장고's Blog</title>
    #     </head>
    #     <body>
    #         <h1>장고's Blog</h1>
    #         안녕하세요 반가워요 Django!!
    #     </body>
    # </html>
    # """)
    #return HttpResponse('blog post_list 뷰 호출')


def post_detail(request,pk):
    print('-----------------------------')
    post = get_object_or_404(Post,pk=pk)
    print(post)
    return render(request,'blog/post_detail.html',{'post':post})
    #return HttpResponse('blog post_detail 뷰 호출하고 {}번 글을 보여줍니다.'.format(pk))

def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            #방법 1)
            # post = Post()
            # post.author = request.user
            # post.title = form.cleaned_data['title']
            # post.text = form.cleaned_data['text']
            # post.published_date = timezone.now()
            # post.save()

            #방법2)
            # post = Post(author=request.user,
            #             title=form.cleaned_data['title'],
            #             text=form.cleaned_data['text'],
            #             published_date=timezone.now())
            # post.save()

            #방법3)
            post = Post.objects.create(author=request.user,
                        title=form.cleaned_data['title'],
                        text=form.cleaned_data['text'],
                        published_date=timezone.now())

            return redirect('post_detail',pk=post.pk)
        # else:  # 검증에 실패하면, form.errors와 form.각필드.errors 에 오류정보를 저장
        #     form.errors
    else:
        form = PostForm()
    return render(request,'blog/post_form.html',{'form':form})

@login_required
def post_new2(request):
    #폼에 내용을 채우고, save 버튼을 클릭 했을때
    if request.method == 'POST':
        form = PostModelForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        #처음에 빈 폼을 보여줄때
        form = PostModelForm()
    return render(request,'blog/post_edit.html',{'form':form})

def post_edit(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == "POST":
        form = PostModelForm(request.POST,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostModelForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_remove(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.delete()
    return redirect('post_list')

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
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)