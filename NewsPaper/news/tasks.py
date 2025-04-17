from celery import shared_task
import datetime
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Post, Category
from django.template.loader import render_to_string


@shared_task
def email_after_create_new(preview, pk, title, subscribers):
    html_content = render_to_string(
    'post_created_email.html',
    {
        'text': preview,
        'link': f'{settings.SITE_URL}/news/news/{pk}'
    }
    )
    
    msg = EmailMultiAlternatives(
        subject = title,
        body = '',
        from_email = settings.DEFAULT_FROM_EMAIL,
        to = subscribers,
    
    )
    
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@shared_task
def every_weekly_notify():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days = 7)
    posts = Post.objects.filter(datetime_in__gte = last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in = categories).values_list('subscribers__email', flat = True))
    html_content = render_to_string(
        'week_posts.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,    
        } 
    )
    
    msg = EmailMultiAlternatives(
         subject = 'Все статьи за неделю',
         body = '',
         from_email = settings.DEFAULT_FROM_EMAIL,
         to = subscribers,
    
    )
    
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    
    
    