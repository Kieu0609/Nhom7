from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,logout,login
from .form import BlogPostForm
from .models import  BlogPost,Comment
from django.views.generic import UpdateView
from django.db.models import Q


def blog(request):
    posts = BlogPost.objects.all()
    posts = BlogPost.objects.filter(status='published').order_by('-dateTime')
    return render(request,"index.html",{'post':posts})


def register(request):
    if request.method=="POST":
        username = request.POST['username']
        name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if password != password1:
          messages.error(request,"mat khau khong phu hop")   
        user = User.objects.create_user(username,email,password)
        user.first_name= name
        user.last_name= last_name
        user.save()
        return redirect ('/login/')
    return render(request,'register.html')

def Login(request):
   if request.method=="POST":
       username = request.POST['username']
       password = request.POST['password']
       user = authenticate(username = username, password = password)
       if user is not None:
          login(request,user)
          return redirect ("/")
       else:
            messages.error(request,"khong thanh cong")
       return render(request,'login.html')
   return render(request,"login.html")

def Logout(request):
    logout(request)
    return redirect('/login')

def add_blogs(request):
    if request.method=="POST":
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.author = request.user
            blogpost.save()
        
            return redirect('/')
    else:
        form=BlogPostForm()
    return render(request, "add_blogs.html", {'form':form})

class UpdatePostView(UpdateView):
    model = BlogPost
    template_name = 'edit_blog_post.html'
    fields = ['title', 'slug', 'content', 'image']
    
def Delete_Blog_Post(request, blog_id):
    posts = BlogPost.objects.get(id=blog_id)
    if request.method == "POST":
        posts.delete()
        return redirect('/')
    return render(request, 'delete_blog_post.html', {'posts':posts})

def Draft(request):
    draft = BlogPost.objects.filter(status='draft')
    return render(request,'draft.html',{'draft_blog':draft})

def Push(request,slug):
    push_ = get_object_or_404(BlogPost,slug =slug)
    push_.status = 'published'
    push_.save()
    return redirect('/')
def view_blog(request,slug):
    post = BlogPost.objects.filter(slug=slug).first()
    comments = Comment.objects.filter(blog=post)
    if request.method=="POST":
        user = request.user
        content = request.POST.get('content','')
        comment = Comment(user = user, content = content, blog=post)
        comment.save()
    #view_blog = BlogPost.objects.filter('-dateTime')
    return render(request,'comment.html',{'post':post, 'comments':comments})

def search(request):   
        searched = request.GET['s']
        blogs = BlogPost.objects.filter(title__contains=searched)
        return render(request, "seach.html", {'s':searched, 'blogs':blogs})

def Delete_Comment(request, blog_id):
    posts = Comment.objects.get(id=blog_id)
    if posts.user == request.user:
        posts.delete()
        blog_id = posts.blog.slug 
    return redirect(f'/view_blog/{blog_id}')
    
       

