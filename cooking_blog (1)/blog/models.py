from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your views here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    image = models.ImageField(upload_to='profile',blank=True,null=True)
    bio = models.TextField()

    def __str__(self):
         return str(self.user)
    
class BlogPost(models.Model):
    
    STATUS_CHOICES = (('draft', 'Draft'),('published', 'Published'),)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft') 

    title=models.CharField(max_length=255)
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    slug=models.CharField(max_length=130)
    content=models.TextField()
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    dateTime=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.author) +  " Blog Title: " + self.title
    def get_absolute_url(self):
        return reverse('blog')
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)   
    dateTime=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username +  " Comment: " + self.content
    





