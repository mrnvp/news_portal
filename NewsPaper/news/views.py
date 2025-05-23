from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.core.cache import cache



class PostList(ListView):
    model = Post
    
    ordering = '-datetime_in'
    template_name = 'news.html'
    context_object_name = 'posts'
    
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        
        if self.request.user.is_authenticated:
             context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        else:
            context['is_not_authors'] = True
            
        return context

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')

    
class PostDetail(DetailView):
    model = Post
    
    template_name = 'new.html'
    context_object_name = 'post'
    queryset = Post.objects.all()
    
    def get_object(self, *args, **kwargs):
        obj = cache.get(f'news-{self.kwargs["pk"]}', None)
        
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'news-{self.kwargs["pk"]}', obj)
        
        return obj
    
class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    
    
    def form_valid(self, form):
        post = form.save(commit=False)
        if 'news' in self.request.path:
            post.type = Post.new
        if 'articles' in self.request.path:
            post.type = Post.paper
        
        post.save()
        form.save_m2m()
        return super().form_valid(form)

class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.changed_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    
    def dispatch(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        print(self.object.name)
        print(self.object.id)
        print(self.object.type)
        print(request.path)
        
        
        if 'news' in request.path and self.object.type != self.object.new:
            raise Http404("Запрошенная новость не найдена.")
        elif 'articles' in request.path and self.object.type != self.object.paper:
            raise Http404("Запрошенная статья не найдена.")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)

        if 'news' in self.request.path:
            post.type = Post.new
        elif 'articles' in self.request.path:
            post.type = Post.paper  

        post.save()

        return super().form_valid(form)

    def get_success_url(self):
        if 'news' in self.request.path:
            return reverse('post_detail', kwargs={'pk': self.object.pk})
        elif 'articles' in self.request.path:
            return reverse('post_detail', kwargs={'pk': self.object.pk})

class PostDelete(DeleteView):
    form = PostForm
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    
    def dispatch(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        
        
        if 'news' in request.path and self.object.type != self.object.new:
            raise Http404("Запрошенная новость не найдена.")
        elif 'articles' in request.path and self.object.type != self.object.paper:
            raise Http404("Запрошенная статья не найдена.")

        return super().dispatch(request, *args, **kwargs)


class CategoryListView(PostList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-datetime_in')
        self.filterset = PostFilter(self.request.GET, queryset)  
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if hasattr(self, 'filterset'):
            context['filterset'] = self.filterset
        
        if hasattr(self, 'category'):
            context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
            context['category'] = self.category
        
        return context
    
@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id = pk)
    category.subscribers.add(user)
    
    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})
    

    

