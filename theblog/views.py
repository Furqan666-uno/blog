from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from .forms import PostForm, EditForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect


def LikeView(request, pk):
    post= get_object_or_404(Post, id= request.POST.get('post_id')) # get_obj_or_404= get elemnt or show 404 error 
    liked= False
    if post.likes.filter(id=request.user.id).exists(): # likes here, we got it from models.py
        post.likes.remove(request.user)
        liked= False
    else:
        post.likes.add(request.user)
        liked= True 
    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)])) # to redirect to same page


class HomeView(ListView):
    model= Post
    template_name= 'home.html'
    ordering= ['-post_date'] # reverse arangement of posts, so that latest post comes first

    def get_context_data(self, *args, **kwargs): # get_context_data provided by django class 
        cat_menu= Category.objects.all()
        context= super(HomeView, self).get_context_data(*args, **kwargs)
        context['cat_menu']= cat_menu
        return context


def CategoryView(request, cats):
    category_posts= Post.objects.filter(category=cats.replace('-', ' ')) # if the catory has dash, it give ' ' there 
    return render(request, 'category.html', {'cats':cats.title().replace('-', ' '), 'category_posts':category_posts}) 


class ArticleDetailView(DetailView):
    model= Post
    template_name= 'article_details.html'

    def get_context_data(self, *args, **kwargs): # this def comes built-in with django  
        # cat_menu= Category.objects.all()
        context= super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        stuff= get_object_or_404(Post, id= self.kwargs['pk'])
        total_likes= stuff.total_likes() # this total_likes from models.py
        liked= False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked= True
        context['total_likes']= total_likes
        context['liked']= liked
        return context


class AddPostView(CreateView):
    model= Post
    form_class= PostForm
    template_name= 'add_post.html'
    # fields= '__all__'

    def get_initial(self):
        initial = super().get_initial()
        initial['author'] = self.request.user.id
        return initial

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AddCommentView(CreateView):
    model= Comment
    form_class= CommentForm
    template_name= 'add_comment.html'
    # fields= '__all__'
    success_url= reverse_lazy('home')

    def form_valid(self, form): # we pass the entire form in here 
        form.instance.post_id= self.kwargs['pk'] # we need this pk bcz we need it for urls 
        return super().form_valid(form)


def CategoryListView(request):
    cat_menu_list= Category.objects.all()
    return render(request, 'category_list.html', {'cat_menu_list':cat_menu_list})


class AddCategoryView(CreateView):
    model= Category
    # form_class= PostForm
    template_name= 'add_category.html'
    fields= '__all__'

    # this is to show all the category we have in navbar dropdown 
    def get_context_data(self, *args, **kwargs): # get_context_data provided by django class 
        cat_menu= Category.objects.all()
        context= super(AddCategoryView, self).get_context_data(*args, **kwargs)
        context['cat_menu']= cat_menu
        return context


class UpdatePostView(UpdateView):
    model= Post
    form_class= EditForm
    template_name= 'update_post.html'
    # fields= ['title', 'title_tag', 'body']


class DeletePostView(DeleteView):
    model= Post
    template_name= 'delete_post.html'
    success_url= reverse_lazy('home') # bcz the normal reverse doesnt work with this for some reason
    # fields= ['title', 'title_tag', 'body']