from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, upgrade_me

NEWS_URL = 'news'

urlpatterns = [
    path(f'{NEWS_URL}/', PostList.as_view(), name = 'post_list'),
    path(f'{NEWS_URL}/<int:pk>', PostDetail.as_view(), name = 'post_detail'),
    path(f'{NEWS_URL}/create/', PostCreate.as_view(), name='news_create'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path(f'{NEWS_URL}/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
    path(f'{NEWS_URL}/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path(f'{NEWS_URL}/upgrade/', upgrade_me, name = 'upgrade')
]
    

