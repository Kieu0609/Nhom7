from django.urls import path
from .import views
from .views import UpdatePostView
urlpatterns = [
    # path("index",views.blog,name="blog")
    path("register/",views.register,name="register"),
    path("login/",views.Login,name="login"),
    path("logout/",views.Logout,name="logout"),

    #blog
    path("",views.blog,name="blog"),
    path("add_blogs/", views.add_blogs, name="add_blogs"),
    path("edit_blog_post/<int:pk>/", UpdatePostView.as_view(), name="edit_blog_post"),
    path("delete_blog_post/<int:blog_id>/", views.Delete_Blog_Post, name="delete_blog_post"),


    path("draft/",views.Draft,name="draft"),
    path("push_blog_post/<str:slug>/",views.Push,name="push_blog_post"),
    path("view_blog/<str:slug>/",views.view_blog,name="view_blog"),
    #path("blog_comments/<slug:slug>/", views.blogs_comments, name="blogs_comments"),

    path("search/",views.search,name="search"),
    path("delete_comment/<int:blog_id>/", views.Delete_Comment, name="delete_comment"),
]