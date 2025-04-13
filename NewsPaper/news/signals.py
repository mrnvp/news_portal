from django.conf import settings
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives

from .models import PostCategory
from django.template.loader import render_to_string

def send_email(preview, pk, title, subscribers):
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
    
    
    

@receiver(m2m_changed, sender = PostCategory)
def notify_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        category = instance.category.all()
        subscribes_emails = []
        
        for cat in category:
            subscribes = cat.subscribers.all()
            subscribes_emails += [s.email for s in subscribes]
    
        send_email(instance.preview(), instance.pk, instance.name, subscribes_emails)
            
            
        
            
            
    